// source.config.ts
import { defineDocs, defineConfig } from "fumadocs-mdx/config";
var docs = defineDocs({
  dir: "content/docs"
});
var source_config_default = defineConfig({
  mdxOptions: {
    // fumadocs default plugins handle TOC, headings, etc.
  }
});
export {
  source_config_default as default,
  docs
};
