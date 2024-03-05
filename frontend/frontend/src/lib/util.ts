import rehypeSanitize from 'rehype-sanitize';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeSlug from 'rehype-slug';
import addClasses from 'rehype-add-classes';
import rehypeShiftHeading from 'rehype-shift-heading';
import rehypeStringify from 'rehype-stringify';
import remarkGfm from 'remark-gfm';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGridTable from '@adobe/remark-gridtables';


// const remarkGridTables = require('remark-grid-tables')
import { unified } from 'unified';
const headingClasses = ' font-extrabold text-gray-900 dark:text-white w-full mt-5';

export const repoRegex = /^[a-zA-Z0-9-_./]+$/;
export function toFixed2(value: any) {
    if (typeof value === 'number') {
        return value.toFixed(2);
    } else {
        return value;
    }
}


export async function processMD(text: string) {
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

