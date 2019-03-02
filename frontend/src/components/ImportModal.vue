<template>
    <b-modal 
        @ok="importPlaylist"
        @cancel="resetModal"
        id="importModal"
        ref="importModal"
        :hide-footer="hideFooter"
        :ok-disabled="disableOK"
        hide-header-close
        centered
    >
        <b-container>
            <span v-if="showInitialMessage"> Swap the playlist <b>{{ playlist.name }}</b> into <b>{{ service.serviceToName }}</b>?</span>
            <span v-else-if="hasError"> {{ errorMessage }} </span>
            <b-img v-else-if="showLoading" center :src="require('../assets/Spinner-1s-200px.gif')" />
        </b-container>
    </b-modal>
</template>

<script>
import URLs from '../service.js'

export default {
    props: {
        playlist: {
            type: Object
        },
        service: {
            type: Object
        }
    },
    data() {
        return {
            showLoading: false,
            hasError: false,
            errorMessage: 'Unable to import playlist'
        }
    },
    computed: {
        showInitialMessage() {
            if(!this.showLoading && !this.hasError){
                return true
            }
        },
        hideFooter(){
            if(this.showLoading){
                return true
            }
        },
        disableOK(){
            if(this.hasError){
                return true
            }
        }
    },
    methods: {
        importPlaylist(event) {
            event.preventDefault()
            this.showLoading = true

            let data = {
                playlist: this.playlist,
                service: this.service
            }

            this.$http.post(URLs.baseURL + 'import', data, {withCredentials: true})
                .then((response) => {
                    this.$refs.importModal.hide()
                    this.showLoading = false
                    this.hasError = false
                })
                .catch((error) => {
                    console.log(error)
                    this.showLoading = false
                    this.hasError = true
                })
        },
        resetModal(){
            this.showLoading = false
            this.hasError = false
        }
    }

}
</script>

<style>

</style>
