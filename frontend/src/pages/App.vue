<template>
  <b-container>
    <Jumbotron/>
    <PlaylistServiceSelect
      @getPlaylists="setPlaylists"
      @getService="setService"
    />
    <PlaylistDisplay
      :playlists="playlists"
      :service="service"
      @loadSelectedPlaylistModal="loadImportModal"
    />
    <ImportModal
      :playlist="selectedPlaylist"
      :service="service"
    >

    </ImportModal>
  </b-container>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import Jumbotron from '../components/Jumbotron.vue'
import PlaylistServiceSelect from '../components/PlaylistServiceSelect.vue'
import PlaylistDisplay from '../components/PlaylistDisplay.vue'
import ImportModal from '../components/ImportModal.vue'
import URLs from '../service.js'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    NavBar,
    Jumbotron,
    PlaylistServiceSelect,
    PlaylistDisplay,
    ImportModal
  },
  data () {
    return {
      playlists: [],
      service: {},
      selectedPlaylist: {}
    }
  },
  methods: {
    setPlaylists(playlists) {
      this.playlists = []
      
      playlists.forEach((playlist) => {
        this.playlists.push(playlist)
      })
    },
    setService(service){
      this.service = service
    },
    loadImportModal(selectedPlaylist) {
      this.selectedPlaylist = selectedPlaylist
      this.service = this.service
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
