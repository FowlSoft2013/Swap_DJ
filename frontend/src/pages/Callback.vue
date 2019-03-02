<template>
    <div class="callback">
        <b-container>
            <b-row align-v="center" align-h="center">
                <b-col md="6" align-self="center" >
                    <p>Authenicating your Spotify Account</p>

                    <b-progress 
                    :value="value"
                    >
                    </b-progress>
                </b-col>
            </b-row>
            
        </b-container> 
    </div>
</template>

<script>
import URLs from '../service.js'

export default{
    data() {
        return {
            value: 0
        }
    },
    methods: {
        incrementValue() {
            setInterval(() => {
                if(this.value < 100){
                    this.value++
                }
            }, 100)
        }
    },
    created () {
        this.incrementValue()

        if(window.location.search){
            const authorizationKeys = window.location.search.substring(1).split('&')
            let authorizationKeysJSON = {}

            authorizationKeys.forEach((key) => {
                const keyName = key.split('=')[0]
                const keyValue = key.split('=')[1]

                authorizationKeysJSON[keyName] = keyValue

                this.$http.get(URLs.baseURL + 'callback?code=' + authorizationKeysJSON['code'], { withCredentials: true}) 
                    .then((response) => {
                        this.value = 100
                        this.$router.push('/')
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            })
        }
    }

}
</script>

<style>
.callback {
    padding: 15em;
}
</style>