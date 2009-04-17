#!/bin/sh

#curl "http://www.fdic.gov/llp/LLPcomments.html" | python get_links.py | xargs -I {} curl http://www.fdic.gov{} -O pdf/
#curl "http://www.fdic.gov/llp/LLPcommentspage2.html" | python get_links.py | xargs -I {} curl http://www.fdic.gov{} -O pdf/
curl "http://www.fdic.gov/llp/LLPcommentspage3.html" | python get_links.py | xargs -I {} curl http://www.fdic.gov{} -O pdf/

mv *.pdf ./pdf
