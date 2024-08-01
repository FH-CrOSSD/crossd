package main

import (
	"encoding/base64"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/pterm/pterm"
	"github.com/pterm/pterm/putils"
)

// getEnvInt is a helper function to get an int value from the environment
func getEnvInt(key string) (parsed int, err error) {
	if value := os.Getenv(key); value == "" {
		err = fmt.Errorf("missing env key %s", key)
	} else if parsed, err = strconv.Atoi(value); err != nil {
		err = fmt.Errorf("cannot parse env key %s=%q: %v", key, value, err)
	}
	return
}

type TemplateFile struct {
	filename string
	items    []TemplateItem
}

type TemplateItem struct {
	replaceToken string
	friendlyName string
	mask         bool
}

var secretTemplates = []TemplateFile{
	{filepath.FromSlash("secret_templates/ghtoken.yaml"), []TemplateItem{{"<github token>", "Github Token", true}}},
	{filepath.FromSlash("secret_templates/redis_auth.yaml"), []TemplateItem{{"<password>", "Redis AUTH password", true}}},
	{filepath.FromSlash("secret_templates/flower_basic_auth.yaml"), []TemplateItem{{"<password>", "Flower HTTP Basic Authentication as user:pw", true}}},
	{filepath.FromSlash("secret_templates/arango-worker-pwd.yaml"), []TemplateItem{{"<username>", "Username for ArangoDB user for worker", false}, {"<password>", "Password for ArangoDB user for worker", true}}},
	{filepath.FromSlash("secret_templates/arango-frontend-pwd.yaml"), []TemplateItem{{"<username>", "Username for ArangoDB user for frontend", false}, {"<password>", "Password for ArangoDB user for frontend", true}}},
	{filepath.FromSlash("secret_templates/arango-root-pwd.yaml"), []TemplateItem{{"<username>", "Username for ArangoDB admin user", false}, {"<password>", "Password for ArangoDB admin user", true}}},
}

var ingressTemplates = []TemplateFile{
	{filepath.FromSlash("ingress_templates/arangodb-ingress.yaml"), []TemplateItem{{"<domain>", "Domain name for the ArangoDB webinterface", false}}},
	{filepath.FromSlash("ingress_templates/flower-ingress.yaml"), []TemplateItem{{"<domain>", "Domain name for the ArangoDB webinterface", false}}},
	{filepath.FromSlash("ingress_templates/frontend-ingress.yaml"), []TemplateItem{{"<domain>", "Domain name for the ArangoDB webinterface", false}}},
	{filepath.FromSlash("ingress_templates/cluster-issuer.yaml"), []TemplateItem{{"<email>", "Email address for Lets Encrypt", false}}},
}

var frontendTemplates = []TemplateFile{
	{filepath.FromSlash("frontend.yaml"), []TemplateItem{{"http://172.23.101.111:30380", "Origin value for CORS as URL (e.g. https://example.com)", false}}},
}

func main() {
	uid, _ := getEnvInt("SUDO_UID")
	gid, _ := getEnvInt("SUDO_GID")

	// seagreen
	title, _ := pterm.DefaultBigText.WithLetters(
		putils.LettersFromStringWithRGB("CrOSSD", pterm.NewRGB(46, 139, 87)),
	).Srender()
	pterm.DefaultCenter.Println(title)
	pterm.DefaultCenter.Println("=== Set up your CrOSSD Microk8s Cluster ===")

	if os.Getuid() != 0 {
		pterm.Error.Println("program was not run as root")
		os.Exit(1)
	}

	pterm.DefaultSection.Println("Requirements")
	pterm.Println("CrOSSD needs the following requirements:")
	putils.BulletListFromStrings([]string{"buildah (via apt)", "microk8s (via snap)"}, "").Render()

	result, _ := pterm.DefaultInteractiveConfirm.WithDefaultText("Install requirements?").Show()
	if result {
		buildahSP, _ := pterm.DefaultSpinner.Start("Installing buildah")
		cmd := exec.Command("apt", "install", "--yes", "buildah")
		stdout, err := cmd.Output()

		if err != nil {
			pterm.Println()
			pterm.Error.Println(err.Error())
			buildahSP.Fail()
			return
		}
		pterm.Println()
		pterm.Println(string(stdout))
		buildahSP.Success()

		pterm.Println()
		mk8SP, _ := pterm.DefaultSpinner.Start("Installing microk8s")
		cmd = exec.Command("/usr/bin/snap", "install", "microk8s", "--classic")
		stdout, err = cmd.CombinedOutput()
		if err != nil {
			pterm.Println()
			pterm.Error.Println(err.Error())
			mk8SP.Fail()
			return
		}
		pterm.Println()
		pterm.Println(string(stdout))
		mk8SP.Success()
		pterm.Success.Println("Finished installing/checking requirements")
	}
	pterm.DefaultSection.Println("Secrets")
	pterm.Println("CrOSSD needs following secrets:")
	pterm.NewStyle(pterm.FgBlue).Sprint("arango-frontend-pwd")
	secrets := []string{pterm.Sprint(pterm.Cyan("arango-frontend-pwd") + " " + pterm.Gray("(username, password)") + ": credentials for ArangoDB for the web interface (ro)"),
		pterm.Sprint(pterm.Cyan("arango-worker-pwd") + " " + pterm.Gray("(username, password)") + ": credentials for ArangoDB for workers (rw)"),
		pterm.Sprint(pterm.Cyan("arango-root-pwd") + " " + pterm.Gray("(username, password)") + ": credentials for ArangoDB admin"),
		pterm.Sprint(pterm.Cyan("flower_basic_auth") + " " + pterm.Gray("(user:password)") + ": credentials for flower queue web interface (" + pterm.NewStyle(pterm.Bold).Sprint("input as user:password") + ")"),
		pterm.Sprint(pterm.Cyan("ghtoken") + ": token used to retrieve GitHub repos (see " + pterm.NewStyle(pterm.FgLightCyan, pterm.Underscore).Sprint("https://fh-crossd.github.io/installation/secrets.html#ghtoken") + ")"),
		pterm.Sprint(pterm.Cyan("redis_auth") + ": password used to authenticate to Redis"),
	}
	putils.BulletListFromStrings(secrets, "").Render()
	empty, err := IsEmpty("secrets")
	if err != nil {
		pterm.Error.Println("Unable to check if secrets directory is empty")
		pterm.Error.Println(err.Error())
		os.Exit(5)
	}
	if !empty {
		pterm.Warning.Println("secrets directory is not empty! Files would be overwritten")
	}
	result, _ = pterm.DefaultInteractiveConfirm.WithDefaultText("Configure secrets?").Show()
	if result {
		err := os.MkdirAll(filepath.FromSlash("secrets"), 0750)
		if err != nil {
			pterm.Error.Printf("Error: %+v\n", err)
			return
		}
		os.Chmod("secrets", 0750)
		processTemplates(secretTemplates, "secrets", transformBase64)

		pterm.Italic.ToStyle().Add(*pterm.FgGray.ToStyle()).Println("secret files can be removed after the cluster was set up")
		pterm.Success.Println("Finished creating secret files")
	}

	syscall.Seteuid(uid)
	syscall.Setegid(gid)
	pterm.DefaultSection.Println("Ingress")
	pterm.Println("Ingress handles public access for CrOSSD web interfaces (TLS certificates, Port 443).")
	pterm.Println("Using our config, every web interface needs a separate sub domain.")
	pterm.Println("As we retrieve TLS certificates va Let's Encrypt, you need to provide an email address.")
	pterm.Println("There are following services:")
	ingresses := []string{pterm.Sprint(pterm.Cyan("arangodb-ingress") + " " + pterm.Gray("(domain)") + ": public domain name for the ArangoDB web interface (e.g. data.example.com)"),
		pterm.Sprint(pterm.Cyan("flower-ingress") + " " + pterm.Gray("(domain)") + ": public domain name for the Flower queue web interface (e.g. queue.example.com)"),
		pterm.Sprint(pterm.Cyan("frontend-ingress") + " " + pterm.Gray("(domain)") + ": public domain name for the CrOSSD health monitor web interface (e.g. crossd.example.com)"),
		pterm.Sprint(pterm.Cyan("cluster-issuer") + " " + pterm.Gray("(email)") + ": email address to use for Let's Encrypt TLS certificates"),
	}
	putils.BulletListFromStrings(ingresses, "").Render()
	empty, err = IsEmpty("ingress")
	if err != nil {
		pterm.Error.Println("Unable to check if ingress directory is empty")
		pterm.Error.Println(err.Error())
		os.Exit(5)
	}
	if !empty {
		pterm.Warning.Println("ingress directory is not empty! Files would be overwritten")
	}
	result, _ = pterm.DefaultInteractiveConfirm.WithDefaultText("Configure ingress (public access for web interfaces via domains)?").Show()
	if result {
		err := os.MkdirAll(filepath.FromSlash("ingress"), 0755)
		if err != nil {
			pterm.Error.Printf("Error: %+v\n", err)
			return
		}
		os.Chmod("ingress", 0755)
		processTemplates(ingressTemplates, "ingress", strings.TrimSpace)

		pterm.Success.Println("Finished creating ingress files")
	}

	pterm.DefaultSection.Println("Frontend Origin")
	pterm.Println("The CrOSSD health monitor web interface needs a valid " + pterm.NewStyle(pterm.Italic).Sprint("Origin") + " for CORS.")
	pterm.DefaultBox.Println(pterm.NewStyle(pterm.Italic).Sprint("CORS (Cross-Origin Resource Sharing) is a security feature that allows web servers \nto specify which origins (domains) are permitted to access their resources."))
	pterm.Println("If the web interface is publicly accessible, you need to use the domain name.")
	pterm.Println("Otherwise an IP address is also possible.")
	pterm.Println("Specify the value as URL like https://example.com.")
	pterm.Println()

	result, _ = pterm.DefaultInteractiveConfirm.WithDefaultText("Configure origin for the frontend?").Show()
	if result {
		processTemplates(frontendTemplates, ".", strings.TrimSpace)
		pterm.Success.Println("Finished configuring origin")
	}

	syscall.Seteuid(0)
	syscall.Setegid(0)
	pterm.DefaultSection.Println("Cluster setup")
	pterm.Println("Setting up the cluster comprises:")
	steps := []string{"Enabling microk8s plugins",
		"Downloading and installing requirements via helm",
		"Loading cluster configuration",
		"Starting pods and services",
	}
	putils.BulletListFromStrings(steps, "").Render()
	result, _ = pterm.DefaultInteractiveConfirm.WithDefaultText("Set up cluster?").Show()
	if result {
		pterm.Info.Println("Enabling microk8s plugins")
		addons := []string{"registry", "dns", "hostpath-storage", "ingress", "cert-manager", "rbac"}
		for _, v := range addons {
			doCommand("microk8s", "enable", v)
		}

		pterm.Info.Println("Retrieving helm charts")
		doCommand("microk8s", "helm", "repo", "add", "cert-manager", "https://charts.jetstack.io")
		doCommand("microk8s", "helm", "repo", "add", "stakater", "https://stakater.github.io/stakater-charts")
		doCommand("microk8s", "helm", "repo", "update")
		cmd := exec.Command("microk8s", "kubectl", "get", "deployment", "crossd-reloader")
		_, err := cmd.CombinedOutput()

		if err == nil {
			pterm.Info.Println("Reloader Deployment already exists")
		} else {
			doCommand("microk8s", "helm", "install", "crossd", "stakater/reloader")
		}

		cmd = exec.Command("microk8s", "kubectl", "get", "deployment", "trust-manager")
		_, err = cmd.CombinedOutput()

		if err == nil {
			pterm.Info.Println("Trust-Manager Deployment already exists")
		} else {
			doCommand("microk8s", "helm", "install", "trust-manager", "cert-manager/trust-manager")
		}

		pterm.Info.Println("Setting up TLS requirements for the cluster (CA, Certs, ...)")
		doCommand("microk8s", "kubectl", "apply", "-f", "certificates/clusterIssuer.yaml", "-f", "certificates/CAIssuer.yaml", "-f", "certificates/CACertificate.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "certificates/trustBundle.yaml", "-f", "certificates/redisCertificate.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "certificates/serviceAccount.yaml", "-f", "certificates/arangoCARole.yaml", "-f", "certificates/roleBinding.yaml", "-f", "certificates/updateArangoCA.yaml")
		time.Sleep(2 * time.Second)

		pterm.Info.Println("Setting up ArangoDB")

		cmd = exec.Command("microk8s", "kubectl", "get", "secret", "arango-ca")
		_, err = cmd.CombinedOutput()

		if err == nil {
			pterm.Info.Println("secret arango-ca already exists")
		} else {
			crtCmd := exec.Command("microk8s", "kubectl", "get", "secret", "root-secret", "--namespace=cert-manager", "-o", "jsonpath={.data['ca\\.crt']}")
			crt, err := crtCmd.Output()
			if err != nil {
				pterm.Println()
				pterm.Error.Println(err.Error())
				os.Exit(2)
			}

			keyCmd := exec.Command("microk8s", "kubectl", "get", "secret", "root-secret", "--namespace=cert-manager", "-o", "jsonpath={.data['tls\\.key']}")
			key, err := keyCmd.Output()
			if err != nil {
				pterm.Println()
				pterm.Error.Println(err.Error())
				os.Exit(2)
			}

			doCommand("microk8s", "kubectl", "create", "secret", "generic", "arango-ca", "--from-literal=ca.crt="+untransformBase64(strings.TrimSpace(string(crt))), "--from-literal=ca.key="+untransformBase64(strings.TrimSpace(string(key))))
		}
		doCommand("microk8s", "kubectl", "apply", "-f", "arango-setup/arango-crd.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "arango-setup/arango-deployment.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "arango-setup/arango-storage.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "arango-setup/arango-storage-role.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "arango-setup/arango-storage-rb.yaml")
		doCommand("microk8s", "kubectl", "apply", "-f", "arango")

		pterm.Info.Println("Loading configs for the cluster")
		doCommand("microk8s", "kubectl", "apply", "-f", "secrets")

		cmd = exec.Command("microk8s", "kubectl", "get", "configmap", "arango-init")
		_, err = cmd.CombinedOutput()

		if err == nil {
			pterm.Info.Println("configmap arango-init already exists")
		} else {
			doCommand("microk8s", "kubectl", "create", "configmap", "arango-init", "--from-file", "arango-init/arango_init.js")
		}

		pterm.Info.Println("Setting up cluster pods and services")
		doCommand("microk8s", "kubectl", "apply", "-f", ".")

		pterm.Success.Println("Instructed microk8s to start up cluster")
		pterm.Info.Println("It might take a while until everthing is up and running")
		pterm.Info.Println("You can check the status of the cluster pods via:")
		pterm.Info.WithMessageStyle(pterm.NewStyle(pterm.Italic, pterm.FgDarkGray)).Println("microk8s kubectl get pods")
	}
}

func doCommand(name string, args ...string) {
	cmd := exec.Command(name, args...)
	stdout, err := cmd.CombinedOutput()

	if err != nil {
		pterm.Println()
		pterm.Println(string(stdout))
		pterm.Error.Println(err)
		os.Exit(2)
	}
	pterm.Println()
	pterm.Println(string(stdout))
}

type fn func(string) string

func processTemplates(templates []TemplateFile, destDir string, transformFn fn) {
	for i := 0; i < len(templates); i++ {
		pterm.Info.Println(templates[i].filename)
		content, _ := os.ReadFile(templates[i].filename)
		for j := 0; j < len(templates[i].items); j++ {
			var mask string = ""
			if templates[i].items[j].mask {
				mask = "*"
			}
			pw, _ := pterm.DefaultInteractiveTextInput.WithDefaultText("Input " + templates[i].items[j].friendlyName).WithMask(mask).Show()
			content = []byte(strings.Replace(string(content), templates[i].items[j].replaceToken, transformFn(pw), -1))
		}
		err := os.WriteFile(filepath.Join(destDir, filepath.Base(templates[i].filename)), content, os.FileMode(0660))
		if err != nil {
			pterm.Error.Printf("Error: %+v\n", err)
			os.Exit(3)
		}
	}
}

func transformBase64(in string) string {
	return strings.TrimSpace(base64.StdEncoding.EncodeToString([]byte(in)))
}

func untransformBase64(in string) string {
	dec, err := base64.StdEncoding.DecodeString(in)
	if err != nil {
		pterm.Error.Println(err.Error())
		os.Exit(4)
	}

	return strings.TrimSpace(string(dec))
}

func IsEmpty(name string) (bool, error) {
	f, err := os.Open(name)
	if err != nil {
		// for some reason, os.open does not return fs.ErrNotExist but syscall.ENOENT as PathError
		if !errors.Is(err, syscall.ENOENT) {
			// error other than dir does not exist
			return false, err
		} else {
			// not existing is treated as empty
			// as dir will be created
			return true, nil
		}
	}
	defer f.Close()

	// get 2 file entries from dir as they should contain a .gitkeep file
	dirs, err := f.Readdirnames(2)
	if err == io.EOF {
		//dir empty
		return true, nil
	} else if err != nil {
		// unable to get files in dir
		return false, err
	}
	empty := true
	for i := 0; i < len(dirs); i++ {
		// check if files other than .gitkeep exist
		if dirs[i] != ".gitkeep" {
			empty = false
		}
	}

	if empty {
		return true, nil
	} else {
		return false, nil
	}
}
