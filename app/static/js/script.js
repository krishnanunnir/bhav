
Vue.component('tablecompnent',{
    template : '<div><h1>This is coming from component</h1></div>'
 });
var app = new Vue({ 
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        stockname:'',
        message: null,
    },
    watch: {
        stockname: function (oldname, newname) {
            console.log(oldname);
            this.debouncedgetStock(oldname);
        }
    },
    created:async function () {
        // delays call to api so as to reduce the number of api call - provided by lodash
        this.debouncedgetStock = _.debounce(this.getStock, 500);
        this.getStock('')
    },
    methods:{
          getStock: async function(stock){
            // if not an empty string we return the searched for value
            if(stock){
                url = "http://127.0.0.1:8000/api/"+stock;
                downloadUrl = "/api/downloads/"+stock;
            }else{
                url = "http://127.0.0.1:8000/api/stonks";
                downloadUrl = "/api/downloads/";
            }
            document.getElementById("downloadhref").href = downloadUrl;
            const response = await fetch(url);
            console.log(response);
            this.message = await response.json();
          }
      }
});