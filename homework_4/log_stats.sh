log_analyze () {
  pattern="^[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}"
  total_queries=$(grep -Ec "$pattern" "$1")
  if [[ "$total_queries" == 0 ]]; then
    >&2 echo "Error in ${1##*/}: no valid entries found"
    exit 1
  fi
  echo "${1##*/}:"
  echo "Total queries: $total_queries"
  echo "--------"
  # Amount of queries by method
  grep -E "$pattern" "$1" | grep -Po "\"\K[[:upper:]]+(?= )" | sort | uniq -c | awk '{ print $2 " - " $1}'
  echo "--------"
  # Top 10 largest queries
  grep -E "$pattern" "$1" | sort -gr --key 10 | awk '{ print $6 " " $7 " " $8 " " $9 " " $10 }' | uniq -c | head |
    awk '{ print $3 " " $5 " " $6 " " $1 }'
  echo "--------"
  # Top 10 client error queries by number of occurrences
  grep -E "$pattern" "$1" | grep -E "\" 4[[:digit:]]{2} " | awk '{ print $7 " " $9 " " $1 }' | sort | uniq -c |
    sort -nr --key 1 | head | awk '{ print $2 " " $3 " " $4 }'
  echo "--------"
  # Top 10 server errors by bytes sent
  grep -E "$pattern" "$1" | grep -E "\" 5[[:digit:]]{2} " | sort | uniq | sort -nr --key 10 | head |
    awk '{ print $7 " " $9 " " $1 }'
  echo "--------"
}

dir_analyze () {
  for file in "$1"/*.log
  do
    log_analyze "$file"
  done
}

if [[ -z "$1" ]]; then
  >&2 echo "Error: no file or directory supplied"
  exit 2
fi

if [[ -n "$2" ]]; then
  output="$2"
else
  output="/dev/stdin"
fi

if [[ -d "$1" ]]; then
  dir_analyze "$1" >> "$output"
else
  log_analyze "$1" >> "$output"
fi

exit 0
