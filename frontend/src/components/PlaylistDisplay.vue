<template>
    <div class="playlist-display">
        <label> 
            Playlists
        </label>
        <b-list-group>
            <PlaylistRow
                v-for="playlist in playlists"
                v-bind:key="playlist.id"
                v-bind:playlist="playlist"
                :service="service"
                @loadSelectedPlaylistModal="loadImportModal"
            >
            </PlaylistRow>
        </b-list-group>
    </div>
</template>

<script>
import PlaylistRow from './PlaylistRow.vue'

export default {
    components: {
        PlaylistRow
    },
    props: {
        playlists: {
            type: Array,
            default: []
        },
        service: {
            type: Object
        }
    },
    methods: {
        loadImportModal(playlist) {
            this.$emit('loadSelectedPlaylistModal', playlist)
        }
    }
}
</script>

<style>
.playlist-display {
    opacity: 0.8;
}
</style>
