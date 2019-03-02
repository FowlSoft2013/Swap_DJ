<template>
    <b-button
        id="apple-music-authorize"
        @click="authorizeAppleMusic"
        class="apple-music-btn"
        :disabled="disabled"
    >
        Apple Music Login
    </b-button>
</template>

<script>
import URLs from '../service.js'

export default {
    methods: {
        authorizeAppleMusic() {
            let music = MusicKit.getInstance()
            music.authorize()
                .then((token) => {
                    const data = {
                        'appleToken': token
                    }

                    this.$http.post(URLs.baseURL + 'apple_music_callback', data, {withCredentials: true}, )
                        .then(() => {
                            this.$emit('authorizedApple')
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                
            })
        }
    },
    props: {
        disabled: {
            type: Boolean
        }
    }
}
</script>

<style>
.apple-music-btn{
    width: 10em;
    background-color: transparent;
    margin: 2%;
}
</style>
