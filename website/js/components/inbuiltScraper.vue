<template lang='pug'>
  span(class="wrapper")
    v-container(column grid-list-md id="page-inbuiltscraper")
    v-layout(column)
      v-flex
        v-card
          v-card-title.display-1.pa-2 Inbuilt AWS Kendra Scrapper
          v-card-text
            h3 This page contains inbuilt webscrapper to be used for automatically building the Kendra documents with the indexes.
      v-flex(v-if="successOutputList.length>0")
        v-card(id="successOutputList")
          v-alert(type="success" :value="successOutputList.length>0" outline) {{successOutputList.join(" ")}}
      v-flex(v-if="errorOutputList.length>0")
        v-card(id="errorOutputList")
          v-alert(type="error" :value="errorOutputList.length>0" outline) {{errorOutputList.join(" ")}}
      v-flex(v-if="warningOutputList.length>0")
        v-card(id="warningOutputList")
          v-alert(type="warning" :value="warningOutputList.length>0" outline) {{warningOutputList.join(" ")}}
      v-flex(v-if="faqScraper.length>0")
        v-card(id="faqscraper")
          v-card-title.headline FAQ Webscraper
          v-card-text
            v-list
              template(v-for="(scraper,index) in faqScraper")
                v-list-tile
                  v-list-tile-content
                    v-list-tile-title {{scraper.name}}
                  v-list-tile-action.job-actions(
                    style="flex-direction:row;"
                  )
                    v-btn(color="primary" @click="run(scraper)") Run 
                v-divider(v-if="index + 1 < faqScraper.length")
      v-flex(v-if="documentScraper.length>0")
        v-card(id="documentscraper")
          v-card-title.headline Document Webscraper
          v-card-text
            v-flex(v-if="documentScraper.length>0")
              template(v-for="(scraper,index) in documentScraper")
                v-card(id="scraper.name" flat)
                  v-card-title.headline {{scraper.name}}
                    v-container
                      v-text-field(label="alias" required v-model="scraper.alias")
                      v-text-field(label="max-items" type="number" required v-model="scraper.max_item")
                      v-text-field(label="metadata-url" required v-model="scraper.metadata_url")
                      v-switch(label="forceCsvSync" v-model="scraper.forceCsvSync")
                  v-card-actions
                    v-btn(color="primary" @click="run(scraper)") Run 
                  v-divider(v-if="index + 1 < documentScraper.length")
</template>

<script>

var Vuex = require("vuex");
var Promise = require("bluebird");
var _ = require("lodash");

export default {
  name: 'inbuiltScrapper',
  data:function(){
    var self = this;
    return {
      documentScraper: [
        { 
          name: 'Blog Scraper', 
          endpoint: "api/runBlogScraper", 
          forceCsvSync: false, 
          alias: "blog-scraper-", 
          metadata_url: "", 
          max_item: 5,
          type: "document"
        }, 
        { 
          name: 'Case Studies Scraper', 
          endpoint: "api/runCaseStudyScraper", 
          forceCsvSync: false, 
          alias: "case-study-scraper-", 
          metadata_url: "", 
          max_item: 5,
          type: "document"
        }
      ],
      faqScraper: [
        { name: 'All FAQ Files', endpoint: "api/runFaqScraper", type: "faq" }
      ],
      errorOutputList: [],
      successOutputList: [],
      warningOutputList: []
    }
  },
  methods: {
    run:async function(scraper){
      let isValidInput = true;
      this.errorOutputList = [];
      this.successOutputList = [];
      this.warningOutputList = [];
      if (scraper.type === "document") {
        isValidInput = this.checkScraper(scraper)
      }
      if (isValidInput) {
        console.log("Running scraper: " + scraper.name)
        console.log(scraper)
        await this.$store.dispatch(scraper.endpoint, scraper).then(
          (data) => {
            console.log("DEBUG: Response data")
            console.log(data)
            if (data.statusCode === 200) {
              if (scraper.type === "document" && data.body !== "") {
                this.successOutputList.push("Job successful. Data Sync ID=" + data.body)
              } else if (scraper.type === "document") {
                this.warningOutputList.push("Nothing to crawl. Are you sure you haven't crawled this?")
              } else {
                this.successOutputList.push("Job successful.");
              }
            } else {
              this.errorOutputList.push("Something went wrong here, please check your query and try again.");
              if (data.status !== 200 && data.hasOwnProperty('message')) {
                this.errorOutputList.push(data.message);
              }
            }
          }
        ).catch(
          (err) => {
            this.errorOutputList.push('Error running ' + scraper.endpoint);
            if (err.hasOwnProperty('message')) {
              this.errorOutputList.push('Error: ' + err.message);
            }
          }
        )
      } else {
        console.log("Invalid input!")
      }
    },
    checkScraper:function(scraper) {
      let isValidAlias = this.aliasCheck(scraper.alias);
      let isValidUrl = this.metadataUrlCheck(scraper.metadata_url);
      let isValidMaxItem = this.maxItemCheck(scraper.max_item);
      return isValidAlias && isValidUrl && isValidMaxItem;
    },
    aliasCheck:function(alias) {
      var regex = /^[a-zA-Z0-9-]+$/;
      if (!alias) {
        this.errorOutputList.push('Alias is required!')
      } else if (alias.search(regex) === -1) {
        this.errorOutputList.push('Alias should only contain alphanumeric characters and hyphens.')
      } else {
        return true;
      }
      return false;
    },
    metadataUrlCheck:function(metadataUrl) {
      if (!metadataUrl) {
        this.errorOutputList.push('Metadata Url is required!')
        return false;
      } else {
        let url;
        try {
          url = new URL(metadataUrl);
        } catch (_) {
          this.errorOutputList.push('Metadata Url is not valid!')
          return false;
        }
        if (url.protocol === "http:" || url.protocol === "https:") {
          return true;
        } else {
          this.errorOutputList.push('Metadata Url not in right protocol (HTTP/HTTPS only)!')
          return false;
        }
      }
    },
    maxItemCheck:function(maxItems) {
      if (!maxItems) {
        this.errorOutputList.push('Max Items is required!')
      } else if (isNaN(maxItems) || maxItems <= 0) {
        this.errorOutputList.push('Max Items is not a valid number.')
      } else {
        return true;
      }
      return false;
    }
  }
}
</script>