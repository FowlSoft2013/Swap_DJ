<template>
    <b-container class="text-center splash-general">
        <b-row class="splash-header">
            <b-col sm>
                <h1>Swap DJ</h1>
            </b-col>
        </b-row>
        <b-row class="splash-info">
            <b-col sm>
                <span> Swap your favorite playlists between the Spotify and Apple Music streaming servives </span>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <span class="auth-info"> Authenicate your services to begin </span>
            </b-col>
        </b-row>
        <b-row class="splash-authenication">
            <b-col sm>
                <SpotifyLogin
                    :disabled="isSpotifyAuth"
                />
            </b-col>
            <b-col sm>
                <AppleMusicLogin
                    :disabled="isAppleAuth"
                    @authorizedApple="disableApple"
                />
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import SpotifyLogin from '../components/SpotifyLogin.vue'
import AppleMusicLogin from '../components/AppleMusicLogin.vue'
import URLs from '../service.js'

export default {
    components: {
        SpotifyLogin,
        AppleMusicLogin
    },
    computed: {
        isFullyAuth() {
            let fullyAuth = false
            if(this.isAppleAuth && this.isSpotifyAuth){
                fullyAuth = true
            }

            return fullyAuth
        }
    },
    watch: {
        isFullyAuth: function (newAuth, oldAuth){
            if(newAuth){
                this.$router.push('/app')
            }
        }
        
    },
    methods: {
        validateSpotifyAuth(){
            return this.$http.get( URLs.baseURL + 'spotify', {withCredentials: true})
        },
        validateAppleMusicAuth(){
            return this.$http.get( URLs.baseURL + 'apple', {withCredentials: true})
        },
        initAuth(){
            return this.$http.all([this.validateAppleMusicAuth().catch(() => { return false }),
                this.validateSpotifyAuth().catch(() => { return false })])
        },
        disableApple() {
            this.isAppleAuth = true
        }
    },
    beforeMount() {
        this.initAuth().then(this.$http.spread((appleResponse, spotifyResponse) => {
            if(appleResponse.status === 200){
                this.isAppleAuth = true
            }

            if(spotifyResponse.status === 200){
                this.isSpotifyAuth = true
            }
        })).then(() => {
            if(this.isFullyAuth){
                this.$router.push('/app')
            }
        })
    },
    data() {
        return {
            isSpotifyAuth:  false,
            isAppleAuth: false,
            authorizedApple: this.appleAuth
        }
    }
}
</script>

<style>
.splash-header{
    padding-top: 10em;
}
.splash-general{
    padding: 1em;
    color: white;
    opacity: 0.8;

}
.splash-info{
    padding: 3em;
    
}
.auth-info{
    width: 50%;
    padding: 1em;
}
.splash-authenication{
    padding-top: 1.5em;
}

</style>
