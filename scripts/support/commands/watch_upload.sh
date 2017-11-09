apt-get install -y inotify-tools

# Upload existing and future pcaps

# Make sure output folder exists
mkdir -p captures

# Upload Existing
for file in captures/*.pcap
do
    post_file '/api-device/device-captures/' "$file" && rm "$file" 
done

# Upload future pcaps (blocking)
inotifywait -m captures/ -e close_write -e move |
    while read path action file; do
        post_capture "$file" && rm "captures/$file" 
    done
