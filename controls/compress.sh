#!/usr/bin/env bash

doit="${1:-false}"

DATA="data"
CONTROLS="$DATA/controls"
LINES="$DATA/lines"
INDEX="-index"


for data in "$CONTROLS" "$LINES" ; do

  # TODO should just first delete empty files
  # then index
  # current code makes no sense

  mkdir -p "$data"
  mkdir -p "$data$INDEX"

  >&2 echo "+ Compressing $data."

  files=( $(ls "$data" | sort -nr) ) # reverse sort numerically
  n=${#files[@]}

  >&2 echo "! There are $n input files."

  d=0
  i=$(( n - 1 ))
  j="$i"

  while [ "$i" -ge 0 -a "$j" -ge 0 ] ; do

    # find the first non empty file
    while [ "$i" -ge 0 ] ; do
      #>&2 echo "( $i )"
      f="$data/${files[$i]}"
      if [ -s "$f" ] ; then
	if [ "$doit" = true ] ; then
	  echo "${files[$i]}" > "$data$INDEX/${files[$i]}"
	fi
	break
      else
	>&2 echo " * File $f is empty deleting"
	if [ "$doit" = true ] ; then
	  rm "$f"
	fi
	i=$(( i - 1 ))
      fi
    done

    j=$(( i - 1 ))

    # compare adjacent files
    while [ "$j" -ge 0 ] ; do
      #>&2 echo "( $i , $j )"

      g="$data/${files[$j]}"

      if [ -s "$g" ] ; then
	if cmp --silent "$f" "$g" ; then
	  >&2 echo " * Files $f and $g are the same, deleting $g."

	  if [ "$doit" = true ] ; then
	    rm "$g"
	    echo "${files[$i]}" > "$data$INDEX/${files[$j]}"
	  fi

	  j=$(( j - 1 ))
	else
	  >&2 echo " * Files $f and $g are different, keeping both."

	  if [ "$doit" = true ] ; then
	    echo "${files[$j]}" > "$data$INDEX/${files[$j]}"
	  fi

	  i="$j"
	  f="$data/${files[$i]}"
	  j=$(( j - 1 ))
	fi
      else
	i="$j"
	break
      fi

    done

  done

done
