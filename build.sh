#!/bin/bash
git clone https://github.com/yuanqing/single-page-markdown-website
npx --yes -- single-page-markdown-website '*.md'
mv build/* ./
rm -rf single-page-markdown-website
open index.html
