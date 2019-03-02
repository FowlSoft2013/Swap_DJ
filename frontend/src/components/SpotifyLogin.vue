<template>
    <b-button 
    :href="authorize_url"
    class="spotify-btn"
    :disabled="disabled"
    >
        Spotify Login
    </b-button>
</template>

<script>
    import URLs from '../service.js'

    export default{
        data () {
            let clientID = 'client_id='
            let responseType = 'response_type=code&'
            let redirectURI = 'redirect_uri=' + URLs.appURL + 'callback&'
            let scope = 'scope=playlist-read-private playlist-modify-public playlist-modify-private user-read-email'

            let authorize_url = 'https://accounts.spotify.com/authorize?'
            authorize_url += clientID
            authorize_url += responseType
            authorize_url += redirectURI
            authorize_url += scope

            return {
                username: '',
                authorize_url: authorize_url
            }
        },
        props:{
            disabled: {
                type: Boolean
            }
        }
    }
</script>

<style>
.spotify-btn{
    width: 10em;
    background-color: transparent;
    margin: 2%;
}
</style>
