## Python Tkinter GUI Tube Downloader
## Download Audio From Your Favorite Youtube Videos


GUI designed with Tkinter
<br><br>
File formats available:
<br>
.wav, .mp3, .m4a
<br><br>
System Requirements:
<br>
Linux OS, Python3, and following packages:
<br>
<code>apt-get install python3-tk</code>
<br>
<code>apt-get install youtube-dl</code>
<br>
<code>apt-get install ffmpeg</code>
<br>
boto3 is required if using the S3 feature:
<br>
pip3 install boto3
<br><br>
Also if using the S3 feature, please ensure your
Amazon keys are set as one of the following:
<br>
<ol>
  <li>
    Environment variables - .bashrc or .bash_profile
    <ul>
      <li><code>export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXX</code></li>
      <li><code>export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXX</code></li>
    </ul>
  </li>
  <li>
    Shared credential file (~/.aws/credentials)
  </li>
  <li>
    AWS config file (~/.aws/config)
  </li>
</ol>
<br
<hr>
<b>Author: James Loye Colley  17DEC2018</b>
