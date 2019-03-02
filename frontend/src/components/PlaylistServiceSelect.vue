<template>
    <b-row>
        <b-col>
            <b-form-select class="playlist-select"
                v-model="selected"
                :options="options"
            >
            </b-form-select>
        </b-col>
            
        <b-col>
        </b-col>
    </b-row>
</template>

<script>
import URLs from '../service.js'

export default {
    data() {
        return {
            selected: null,
            options: [
                { value: null, text: 'Select a service', disabled: true },
                { value: 0, text: 'Spotify'},
                { value: 1, text: 'Apple Music'}
            ]
        }
    },
    watch: {
        selected() {
            this.getPlaylists()
        }
    },
    methods: {
        getPlaylists () {
            const SPOTIFY = "0"
            const APPLE_MUSIC = "1"
            const NONE = null
            let service = {}

            if(this.selected == SPOTIFY){
                this.$http.get(URLs.baseURL + 'playlists', {withCredentials: true})
                    .then((response) =>{
                        this.$emit('getPlaylists', response.data.items)
                        service.serviceFromName = 'Spotify'
                        service.serviceFromValue = 0
                        service.serviceToName = 'Apple Music'
                        service.serviceToValue = 1
                        this.$emit('getService', service)
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
            else if(this.selected == APPLE_MUSIC){
                this.$http.get(URLs.baseURL + 'apple_playlists', {withCredentials: true})
                    .then((response) =>{
                        let playlists = []
                        response.data.data.forEach((item) => {
                            let description = item.attributes.description == undefined ? "" : item.attributes.description.standard
                            let playlist = {
                                id: item.id,
                                name: item.attributes.name,
                                href: item.href,
                                description: description
                            }

                            playlists.push(playlist)
                        })

                        this.$emit('getPlaylists', playlists)
                        service.serviceFromName = 'Apple Music'
                        service.serviceFromValue = 1
                        service.serviceToName = 'Spotify'
                        service.serviceToValue = 0
                        this.$emit('getService', service)
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        }
    }

}
</script>

<style>
.playlist-select {
    opacity: .80;
}
</style>
