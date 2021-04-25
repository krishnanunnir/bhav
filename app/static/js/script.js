
// delimiter needed to be added since there would be a conflict with the template syntax of Django
var app = new Vue({ 
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        stockname:'',
        message: null,
        total_page_count: 1,
        page_number: 1,
        loading: false,
        lastdate:''
    },
    watch: {
        stockname: function (oldname, newname) {
            this.page_number =1; // if stock name updated we should start at pagenumber 1
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
            // if not an empty string for stockname we return the searched for value
            // in case of empty string we return the whole dataset

            // regex to check if input stockname is valid
            var re = new RegExp("^([a-z0-9 ]*)$");

            // handling everything in lowercase
            stock = stock.toLowerCase();

            // handles if pagenumber decreased beyond zero
            if(this.page_number <= 0){
                this.page_number = 1;
            }
            // handles if pagenumber incremented beyond totalpage count
            if(this.page_number > this.total_page_count){
                this.page_number = this.total_page_count;
            }
            this.loading=true;
            if(stock){
                if(!re.test(stock)){
                    // stock names cannot have special character so returning to null
                    // this avoids a ton of issues by handling here
                    this.message=[]
                    return ;
                }
                // url for api call that returns the search result
                // the result is paginated and can be accessed by the page parameter in url
                url = "api/search?stockname="+stock+"&page="+this.page_number;

                // url to download the search result as a zip
                downloadUrl = "/downloads/"+stock;
            }else{
                // same steps as above repated for entire dataset
                url = "api/stonks?page="+this.page_number;
                downloadUrl = "/downloads/";
            }

            // updating the download url as the one obtained above - can it be updated directly?
            document.getElementById("downloadhref").href = downloadUrl;

            // api headers added - the type need to be defined here
            const response = await fetch(url,{
                method:'GET',
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            });
            // updating various values with input from 
            var jsondata = await response.json();
            this.message = jsondata.results;
            this.total_page_count = jsondata.total_pages;
            this.lastdate = jsondata.updated_on;
            this.loading=false;
          }
      }
});