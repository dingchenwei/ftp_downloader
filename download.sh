strings=("label" "matte" "temp_matte" "guided_result" "add")
for str in ${strings[@]}; do
  python download_ftp.py "$str" &
done
