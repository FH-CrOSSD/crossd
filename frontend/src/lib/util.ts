import remarkGridTable from '@adobe/remark-gridtables';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import addClasses from 'rehype-class-names';
import rehypeKatex from 'rehype-katex';
import rehypeSanitize from 'rehype-sanitize';
import rehypeShiftHeading from 'rehype-shift-heading';
import rehypeSlug from 'rehype-slug';
import rehypeStringify from 'rehype-stringify';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import { unified } from 'unified';

// tailwindcss classes for the metric headings
const headingClasses = ' font-extrabold text-gray-900 dark:text-white w-full mt-5';
// regex used to validate Github owner/name combinations
export const repoRegex = /^[a-zA-Z0-9-_./]+$/;
// results per page for the search pagination
export const PER_PAGE = 10;

export function toFixed2(value: any) {
    // limit to 2 decimals or 0 if integer
    if (typeof value === 'number') {
        return value % 1 === 0 ? value : value.toFixed(2);
    } else {
        return value;
    }
}

export async function processMD(text: string) {
    // convert markdown to html via remark/rehype
    const file = await unified()
        .use(remarkParse)
        .use(remarkMath)
        .use(remarkGfm)
        .use(remarkGridTable)
        .use(remarkRehype)
        .use(rehypeSanitize)
        .use(rehypeKatex)
        .use(rehypeSlug)
        .use(rehypeAutolinkHeadings)
        .use(rehypeShiftHeading, { shift: 1 })
        .use(addClasses, {
            p: 'text-base text-gray-900 dark:text-white leading-normal font-normal text-left whitespace-normal afterp',
            h1: 'text-5xl' + headingClasses,
            h2: 'text-4xl metric_heading' + headingClasses,
            h3: 'text-3xl' + headingClasses,
            h4: 'text-2xl' + headingClasses,
            h5: 'text-xl' + headingClasses,
            h6: 'text-lg' + headingClasses,
            blockquote: "font-semibold text-gray-900 dark:text-white text-left text-lg bg-gray-50 dark:bg-gray-800 border-s-4 border-gray-300 dark:border-gray-500 italic p-4 my-4"
        })
        .use(rehypeStringify)
        .process(text.replaceAll('$$', ' $'));
    return file;
}

export let bakGenericDataFn = (category: string, project_id: string, entry: string | null = null, data: any) => {
    return (selected: number) => {
        if (entry) {
            return data[selected]?.[category][project_id][entry] ?? null;
        } else {
            return data[selected]?.[category][project_id] ?? null;
        }
    };
};