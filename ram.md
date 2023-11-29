Docker arguments:
-p 8080:8080
-v /Users/ram/ABHero/webarchive-data/:/webarchive
-e INIT_COLLECTION=my-web-archive

conda activate abhera, cd pywb && cd vueui && yarn && cd .. && cd ..
wayback --record --live

cd pywb && cd vueui && yarn build && cd .. && cd .. && pip uninstall pywb -y && python setup.py install && wayback --record --live

removed srcset from html_rewriter

update head_insert.html

Shopify images don't work so make sure it works for ecommerce like them

test at http://localhost:8080/live/https://boxbox.in/products/formula-1-tyres-t-shirt
