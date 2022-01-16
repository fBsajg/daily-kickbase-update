### Daily Kickbase Team Update

- script is made for use on remote server running as daily cronjob

- install Kickbase-API==0.0.8
- set username and password in `kb.py`

kickbase.txt is created as formatted html ready to send as mail from **remote server** to your mailadress.

**Example**

create `template.txt`

To: *yourmailadress*

Subject: Kickbase Update

From: *name@yourserver.com*

MIME-Version: 1.0

Content-Type: text/html; charset="utf-8"

Content-Transfer-Encoding: 8BIT

Content-Disposition: inline

**doKickbaseUpdate.sh**

`python3 ~/dev/kickbase/kb.py`

`cat ~/template.txt ~/kickbase.txt > ~/mail.txt`

`/usr/sbin/sendmail -vt < ~/dev/kickbase/mail.txt`

**CRONJOB**

`30 4 * * * /bin/sh /home/doKickbaseUpdate.sh 1> /home/kickbase.log 2> /home/kickbase_err.log`




