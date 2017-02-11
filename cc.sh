#!/usr/bin/env bash
# cc: Commit changes.
description=$1

number_of_unpushed_commits=$(git cherry | wc -l)

if [[ "$number_of_unpushed_commits" -gt 0  ]];
then
  echo "You should first stash or push previous commits."
else
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
fi
