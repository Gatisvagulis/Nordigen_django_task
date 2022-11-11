# Nordigen_django_task
<h1>Connect django app with Nordigen API to fetch data from different banks</h2>
<ol>
  <li>To start the app first you need to create an account and generate keys here: https://nordigen.com/ . Then add these keys in .env file.</li>
  <li>Go to main project url "domainname.com/"(this is an example domain name): when the access token and refresh token are empty users generate them here.</li>
  <li>Both tokens from the point above should be saved under .env file ACCESS_TOKEN and REFRESH_TOKEN.</li>
  <li>Restart the server and refresh the browser and you are good to go.</li>
  <li>Now you can start connecting your banks.</li>
  <li>To access premium products you have to ask dirrect to sales@nordigen.com</li>
</ol>
<p><b>Side note: </b>In project we use Celery to get data async. You have to activate redis-cli.exe file on your computer.</p>
