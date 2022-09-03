git add .
echo "Enter commit message: "
read -r message
echo "The commit message is: $message"
git commit -am "$message"
git push origin master
