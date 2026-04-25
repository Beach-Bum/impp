import { docs } from '@/.source';
import { loader } from 'fumadocs-core/source';

// fumadocs-mdx v11 returns files as a lazy function; fumadocs-core v15 needs an array
const _src = docs.toFumadocsSource();
const _files = typeof _src.files === 'function' ? (_src.files as () => unknown[])() : _src.files;

export const source = loader({
  baseUrl: '/docs',
  source: { ..._src, files: _files as Parameters<typeof loader>[0]['source']['files'] },
});
