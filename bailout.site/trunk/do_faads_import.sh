var0=0
LIMIT=1000

while [ "$var0" -lt "$LIMIT" ]
#      ^                    ^
# Spaces, because these are "test-brackets" . . .
do
  echo "running loop $var0..."
  ./manage.py do_faads_import
  var0=`expr $var0 + 1`
done

echo

exit 0