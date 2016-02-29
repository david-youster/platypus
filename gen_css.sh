#!/usr/bin/env bash

SCSS_DIR=scss
CSS_DIR=static/styles

INFILE=web.scss
OUTFILE=web.css

sass  "$SCSS_DIR/$INFILE" "$CSS_DIR/$OUTFILE" 