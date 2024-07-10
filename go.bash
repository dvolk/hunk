set -e
set -x

echo "generating new deployment..."
python3 main.py

echo "deleting existing deployment..."
sudo rm -rf /var/www/html/dev.oxfordfun.com || true

echo "copying new deployment..."
sudo cp -r deploy/dev.oxfordfun.com/ /var/www/html
