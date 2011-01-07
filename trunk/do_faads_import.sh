var0=0
LIMIT=1000

control_c()
# run if user hits control-c
{
  exit $?
}
 
# trap keyboard interrupt (control-c)
trap control_c SIGINT

while [ "$var0" -lt "$LIMIT" ]
#      ^                    ^
# Spaces, because these are "test-brackets" . . .
do
  echo "running loop $var0..."
  ./manage.py faads_import
  var0=`expr $var0 + 1`
done

echo

exit 0
