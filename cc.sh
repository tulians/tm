#!/usr/bin/env bash
# cc: Commit changes.
description=$1

git add .
git status

echo "Commit description: '$description'"

read -p "Is the commit description correct? [y/n]: " prompt

if [[ ("$prompt" == "Y") || ("$prompt" == "y") ]];
then
  git commit -m "$description"
  git push origin master
else
  echo "Run the command again with the correct commit description."
fi
