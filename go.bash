set -e
set -x

echo "generating new deployment..."
python3 main.py

for dir in deploy/*/; do
    dirname=$(basename $dir)

    echo "deleting existing deployment for $dir..."
    sudo rm -rf /var/www/html/$dirname || true

    echo "copying new deployment for $dir..."
    sudo cp -r $dir /var/www/html

done;
