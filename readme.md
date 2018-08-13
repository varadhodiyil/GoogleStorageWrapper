# GOOGLE STORAGE WRAPPER
Includes complete package for Google Bucket Storage.
## GoogleStorage
1. creating bucket
2. uploading object.
3. deleting object.

## GoogleAuthenticateReader
1. Generate Signed URL

## PIP installation
```
pip install git+https://github.com/sachinedward/GoogleStorageWrapper.git
```
## Code Usage:
### GoogleStorage
```
from GoogleStorage.Google_Storage import GoogleStorage
gs = GoogleStorage('/Desktop/GoogleAuth.json')
gs.setBucketName('test')
gs.upload_object(...) # upload file
```

### GoogleAuthenticateReader
```
from GoogleStorage.GoogleAuthenticateReader import GoogleAuthenticateReader
gs = GoogleAuthenticateReader('/Desktop/GoogleAuth.json')
gs.generate_signed_url('gs://xzy/test/test.pdf') # gs url
```

## Author
* **Sachin Edward** - (https://www.linkedin.com/in/sachinedward/)
* **Madhan Varadhodiyil**