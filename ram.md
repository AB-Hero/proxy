Docker arguments:
-p 8080:8080
-v /Users/ram/ABHero/webarchive-data/:/webarchive
-e INIT_COLLECTION=my-web-archive

conda activate abhera, cd pywb && cd vueui && yarn && cd .. && cd ..
wayback --record --live

cd pywb && cd vueui && yarn build && cd .. && cd .. && pip uninstall pywb -y && python setup.py install && wayback --record --live

update head_insert.html
