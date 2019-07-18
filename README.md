# Vue

### setting package.json

    {
      "name": "vue_demo",
      "version": "0.0.1",
      "description": "vue-demo",
      "scripts": {
        "build:vue": "parcel build ./index.js --public-url .",
        "start": "concurrently --kill-others 'yarn run start:django' 'yarn run watch:vue'",
        "start:django": "python manage.py runserver",
        "start:vue": "parcel dist/index.html",
        "watch:vue": "parcel watch ./index.js --public-url ."
      },
      "author": "",
      "license": "All rights reserved",
      "private": true,
      "devDependencies": {
        "@vue/component-compiler-utils": "^2.6.0",
        "concurrently": "^4.1.0",
        "parcel": "^1.12.0",
        "vue": "^2.6.10",
        "vue-hot-reload-api": "^2.3.3",
        "vue-template-compiler": "^2.6.10"
      },
      "dependencies": {
        "axios": "^0.18.0",
        "babel-polyfill": "^6.26.0",
        "semantic-ui-offline": "^2.4.1",
        "vue-js-modal": "^1.3.31",
        "vue-picture-input": "^2.1.6",
        "vue-router": "^3.0.6",
        "vuex": "^3.1.1"
      }
    }
    
##
### Run Vue watch and Django server
`yarn build:vue`  
`yarn watch:vue`  
`yarn start:django`


# PWA
### install
`pip install django-progressive-web-app`  

### add in settings.py(vue_demo/settings.py)
    
    INSTALLED_APPS = [
    ...
    ...
    'pwa',
    ]
##
### add urls in urls.py
    urlpatterns = [
        ...
        path("", views.index),
        path("base_layout",views.base_layout),
        path("getdata",views.getdata),
        path("",include('pwa.urls'))
    ]
##
### **create serviceworker**
#### **Setting.py**

    PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'app/static', 'serviceworker.js')
#### **serviceworker.js**
    
    var staticCacheName = 'djangopwa-v2';
    self.addEventListener('install', function(event) {
      event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
          return cache.addAll([
            '/base_layout',
            '',
            './static/index.js',
            './static/src/worldwide-72.png'
          ]);
        })
      );
    });
    
    self.addEventListener('fetch', function(event) {
      var requestUrl = new URL(event.request.url);
        if (requestUrl.origin === location.origin) {
          if ((requestUrl.pathname === '/')) {
            event.respondWith(caches.match('/base_layout'));
            return;
          }
        }
        event.respondWith(
          caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
          })
        );
    });
##
### add manifest.json
#### **create at templates directory**

    {
    "name": "Summer Vue Demo",
    "short_name": "summer_vue_demo",
    "description": "demo pwa with django and vue.js",
    "start_url": "/base_layout",
    "scope": ".",
    "background_color": "#EEE",
    "theme_color": "#4A148C",
    "display": "standalone",
    "orientation": "portrait-primary",
    "dir":"ltr",
    "icons": [
      {
        "src": "./static/src/worldwide-72.png",
        "type": "image/png",
        "sizes": "72x72"
      },{
        "src": "./static/src/worldwide-144.png",
        "type": "image/png",
        "sizes": "144x144"
      },{
        "src": "./static/src/worldwide-256.png",
        "type": "image/png",
        "sizes": "256x256"
      },{
        "src": "./static/src/worldwide-512.png",
        "type": "image/png",
        "sizes": "512x512"
      }
     ]
    }

## **Indexed Database**
#### add tag and script in base.html
    {% load pwa %}
    {% progressive_web_app_meta %}

    <script type="text/javascript" src="./static/idb.js"></script>
    <script type="text/javascript" src="./static/idbop.js"></script>
also add div to display result
    
    <div id="offlinedata">
    </div>

#### **create idb.js at static directory**  
copy from [this](https://github.com/kirankumbhar/DjangoPWA/blob/master/posts/static/js/idb.js)  

#### **create idbop.js at static directory**

    
	var dbPromise = idb.open('feeds-db', 5, function(upgradeDb) {
		upgradeDb.createObjectStore('feeds',{keyPath:'pk'});
	});
	fetch('https://localhost/getdata').then(function(response){
		return response.json();
	}).then(function(jsondata){
		dbPromise.then(function(db){
			var tx = db.transaction('feeds', 'readwrite');
	  		var feedsStore = tx.objectStore('feeds');
	  		for(var key in jsondata){
	  			if (jsondata.hasOwnProperty(key)) {
			    	feedsStore.put(jsondata[key]);
			  	}
	  		}
		});
	});
	var post="";
	dbPromise.then(function(db){
		var tx = db.transaction('feeds', 'readonly');
  		var feedsStore = tx.objectStore('feeds');
  		return feedsStore.openCursor();
	}).then(function logItems(cursor) {
		  if (!cursor) {
		  	//if true means we are done cursoring over all records in feeds.
		  	document.getElementById('offlinedata').innerHTML=post;
		    return;
		  }
		  for (var field in cursor.value) {
		    	if(field=='fields'){
		    		feedsData=cursor.value[field];
		    		for(var key in feedsData){
		    			if(key =='title'){
		    				var title = '<h3>'+feedsData[key]+'</h3>';
		    			}
		    			if(key =='author'){
		    				var author = feedsData[key];
		    			}
		    			if(key == 'body'){
		    				var body = '<p>'+feedsData[key]+'</p>';
		    			}
		    		}
		    		post=post+'<br>'+title+'<br>'+author+'<br>'+body+'<br>';
		    	}
		    }
		  return cursor.continue().then(logItems);
		});
		

##
### ...Setting nginx... 
put cert in project directory

#### DEMO
1. run nginx
2. parcel watch  

        parcel watch index.js --cert localhost.pem --key localhost-key.pem
    
