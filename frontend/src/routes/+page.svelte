<script>
    import axios from 'axios';

    const query = "Inception";
    const apiKey = import.meta.env.VITE_TMDB_KEY;

    console.log(apiKey);

    const baseUrl = "https://api.themoviedb.org/3";

    axios
    .get(`${baseUrl}/search/movie`, {
      params: {
        api_key: apiKey,
        query: query,
      },
    })
    .then((response) => {
      console.log("Search results:", response.data);
    })
    .catch((error) => {
      console.error("Error fetching data:", error.message);
    });
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>


