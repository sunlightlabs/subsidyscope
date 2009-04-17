#!/bin/sh
rm comments.txt
touch comments.txt
find ./pdf | xargs -I {} pdftotext {} - >> comments.txt