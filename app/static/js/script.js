
Vue.component('tablecompnent',{
    template : '<div><h1>This is coming from component</h1></div>'
 });
var app = new Vue({ 
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        stockname:'',
        message: null,
        total_page_count: 1,
        page_number: 1,
        loading: false
    },
    watch: {
        stockname: function (oldname, newname) {
            this.page_number =1;
            this.debouncedgetStock(oldname);
        },
        page_number: function(oldval, newval){
            this.debouncedgetStock(this.stockname);
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
            // in case of empty string we return the whole dataset
            if(this.page_number <= 0){
                this.page_number = 1;
            }
            if(this.page_number > this.total_page_count){
                this.page_number = this.total_page_count;
            }
            this.loading=true;
            if(stock){
                url = "http://127.0.0.1:8000/api/"+stock+"?page="+this.page_number;
                downloadUrl = "/api/downloads/"+stock;
            }else{
                url = "http://127.0.0.1:8000/api/stonks?page="+this.page_number;
                downloadUrl = "/api/downloads/";
            }
            document.getElementById("downloadhref").href = downloadUrl;
            const response = await fetch(url,{
                method:'GET',
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            });
            var jsondata = await response.json();
            console.log(jsondata)
            this.message = jsondata.results;
            this.total_page_count = jsondata.total_pages;
            this.loading=false;
            // console.log(this.message);
          }
      }
});