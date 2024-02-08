Docker arguments:
-p 8080:8080
-v /Users/ram/ABHero/webarchive-data/:/webarchive
-e INIT_COLLECTION=my-web-archive

conda activate abhera, cd pywb && cd vueui && yarn && cd .. && cd ..
wayback --record --live

cd pywb && cd vueui && yarn build && cd .. && cd .. && pip uninstall pywb -y && python setup.py install && wayback --record --live

test with buzzbonus.html
update head_insert.html

Shopify images don't work, so removed srcset from html_rewriter

test at http://localhost:8080/live/https://boxbox.in/products/formula-1-tyres-t-shirt

Build Docker with:

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 679946893962.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform linux/amd64 --no-cache -t proxy:latest . --load
docker tag proxy:latest 679946893962.dkr.ecr.us-east-1.amazonaws.com/proxy:latest
docker push 679946893962.dkr.ecr.us-east-1.amazonaws.com/proxy:latest

Deploy with apprunner
Go to https://guyv6arqp9.us-east-1.awsapprunner.com/

bad sites: jess.travel (working), phind.com, braze.com, fearofgod.com, test on contact_info
Get to this level: https://youtube.com/watch?v=fheibWCUPJ8, Optimizely Web Experimentation, https://support.optimizely.com/hc/en-us/articles/4410288109197-Get-started-with-Optimizely-Web-Experimentation, create script later and disclaimer that it doesn't work perfectly until you install script

Debug browser out of date:
navigator.appVersion
