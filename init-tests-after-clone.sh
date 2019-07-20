#!/bin/bash -e

if [[ -z "$TRAVIS" ]]; then
  read -p "This operation will destroy locally modified files. Continue ? [N/y]: " answer
  if [[ ! $answer =~ [yY] ]]; then
    exit 2
  fi
fi

git checkout -b __test_branch__
git tag __testing_point__
git checkout master || git checkout -b master
git reset --hard HEAD~1
git reset --hard HEAD~1
git reset --hard HEAD~1
git reset --hard __testing_point__
git checkout __test_branch__
