<template>
    <div id="display">
        {{ value }}
    </div>
</template>

<script>
    export default {
        name: "App",
        data () {
            return {
                value: "Where Vue is,change when no service worker ",
            }
        }

    }
</script>

<style scoped>
#display{
    border: 1pt solid;
    background-color: black;
    color: lightgreen;
}
</style>