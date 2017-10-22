Geocity Module Repository
=========================

This simple project is an example to show proxmity on the cities given its geo latitude and longitude location.  And also do keyword querying on the cities.

Approach:
---------------
Used Flask for web routes as to create Rest API for this project.  Geo-city info was parsed and set to a user-defined class type representation.  Stored info in a dictionary for indexing.  This can carry over to big data with data warehousing techniques and cached using popular tools such as Whoosh, Apache-Lucene, solr, etc., but it's not in the scope here.  


Steps:
--------
1. git clone https://github.com/thanhn9/geocity.git
2. cd geocity
3. make install
4. make test
5. make run

Please refer to document "apidoc.docx" for API info.
                         
For a UI to the Rest API calls, I think Postman did a good job.  Can refer to https://www.getpostman.com/.  At times, I used Python requests module and/or a browser will do, as these activities are mainly refered to the GET method.

---------------


✨🍰✨
