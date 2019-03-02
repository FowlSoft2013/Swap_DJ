<template>
    <div>
        <b-list-group-item variant="light">
            <b-row>
                <b-col>
                    <b-link
                        v-b-modal.importModal
                        @click="loadImportModal"
                    > 
                        {{ playlist.name }} 
                    </b-link>
                </b-col>
                
                <b-col>
                    
                </b-col>
            </b-row>
        </b-list-group-item>
    </div>
</template>

<script>
export default {
    props: {
        playlist: {
            type: Object
        },
        service: {
            type: Object
        }
    },
    methods: {
        loadImportModal() {
          this.$emit('loadSelectedPlaylistModal', this.playlist)
        }
    }
}
</script>

<style>

</style>
