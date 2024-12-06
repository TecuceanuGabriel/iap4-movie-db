<script>
    import {
        apiKey,
        imgBaseUrl,
        imgSizeSmall,
        redirectTo,
        getMovieGenres,
        getTVGenres,
    } from "$lib/utils.ts";
    import { onMount } from "svelte";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Button } from "$lib/components/ui/button/index.js";

    import File from "lucide-svelte/icons/file";
    import House from "lucide-svelte/icons/house";
    import ChartLine from "lucide-svelte/icons/chart-line";
    import ListFilter from "lucide-svelte/icons/list-filter";
    import Ellipsis from "lucide-svelte/icons/ellipsis";
    import Package from "lucide-svelte/icons/package";
    import Package2 from "lucide-svelte/icons/package-2";
    import PanelLeft from "lucide-svelte/icons/panel-left";
    import CirclePlus from "lucide-svelte/icons/circle-plus";
    import Search from "lucide-svelte/icons/search";
    import Settings from "lucide-svelte/icons/settings";
    import ShoppingCart from "lucide-svelte/icons/shopping-cart";
    import UsersRound from "lucide-svelte/icons/users-round";

    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Sheet from "$lib/components/ui/sheet/index.js";
    import * as Table from "$lib/components/ui/table/index.js";
    import * as Tabs from "$lib/components/ui/tabs/index.js";
    import * as Tooltip from "$lib/components/ui/tooltip/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index";
    import { Separator } from "$lib/components/ui/separator";

    let searchQuery = "";
    let timeout;
    let searchResult = [];
    let showResults = false;
    let mediaGenres = new Map();

    // Function that gets triggered when the input changes
    function handleInputChange(event) {
        // Clear the previous timeout to restart the debouncing
        clearTimeout(timeout);

        // Set a new timeout to fire the function after 500ms (half a second)
        timeout = setTimeout(async () => {
            if (searchQuery.trim()) {
                try {
                    const response = await fetch(
                        `${apiKey}/search/multi/${searchQuery}/1`,
                    );

                    if (!response.ok) {
                        throw new Error(
                            `Could not get query: ${response.status}`,
                        );
                    }

                    const data = await response.json();
                    searchResult = data.results.map((element) => {
                        let name = null;
                        let imageUrl = `${imgBaseUrl}/${imgSizeSmall}`;
                        let releaseDate = null;
                        let genres = [];
                        switch (element.media_type) {
                            case "movie":
                                name = element.title;
                                releaseDate = element.release_date;
                                if (element.poster_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.poster_path}`;
                                }
                                genres = element.genre_ids;
                                break;
                            case "tv":
                                name = element.name;
                                releaseDate = element.first_air_date;
                                if (element.poster_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.poster_path}`;
                                }
                                genres = element.genre_ids;
                                break;
                            case "person":
                                name = element.name;
                                if (element.profile_path === null) {
                                    imageUrl = null;
                                } else {
                                    imageUrl = `${imageUrl}/${element.profile_path}`;
                                }
                                break;
                            default:
                                imageUrl = null;
                                break;
                        }
                        return {
                            name: name,
                            imageUrl: imageUrl,
                            releaseDate: releaseDate,
                            type: element.media_type,
                            genres: genres.map((id) => mediaGenres.get(id)),
                            id: element.id,
                        };
                    });
                } catch (e) {
                    console.log(e);
                }
            } else {
                searchResult = [];
            }
        }, 1000);
    }

    let searchBar;
    onMount(async () => {
        let movieGenresArray = await getMovieGenres();
        let tvGenresArray = await getTVGenres();
        movieGenresArray.forEach((element) => {
            mediaGenres.set(element.id, element.name);
        });
        tvGenresArray.forEach((element) => {
            mediaGenres.set(element.id, element.name);
        });

        document.addEventListener("click", (event) => {
            if (!searchBar.contains(event.target)) showResults = false;
        });
        return () => {
            document.removeEventListener("click", handleClickOutside);
        };
    });
</script>

<header
    class="relative z-10 w-full mr-auto ml-auto px-10 pt-8 z-30 flex items-start"
>
    <div class="relative top-0 mr-auto text-left">
        <a
            href="/"
            style="font-family: 'Open Sans';
        font-weight: 700;">Taped</a
        >
    </div>
    <div bind:this={searchBar} class="relative flex-1 grow-0">
        <Search class="absolute left-2.5 top-2.5 h-4 w-4" />
        <Input
            type="search"
            class="transition-all text-white border-none bg-background/5 focus:bg-background/40 w-full rounded-lg pl-8
            w-[150px] sm:w-[300px] md:w-[400px] lg:w-[700px]"
            bind:value={searchQuery}
            on:input={handleInputChange}
            on:focus={() => (showResults = true)}
        />

        {#if showResults && searchResult.length > 0}
            <ScrollArea
                class="absolute w-full left-0 select-none rounded-md backdrop-blur-lg flex max-h-72 flex-col overflow-y-auto"
                style="font-family: 'Open Sans';"
            >
                {#each searchResult as result}
                    <div
                        tabindex="0"
                        role="button"
                        class="cursor-pointer transition-all flex flex-row p-3 bg-rich_black/70 hover:bg-rich_black/40 text-white"
                        on:click={() =>
                            redirectTo(`/${result.type}/${result.id}`)}
                        on:keydown={(event) => {
                            if (event.key === "Enter") {
                                redirectTo(`/${result.type}/${result.id}`);
                            }
                        }}
                    >
                        {#if result.imageUrl === null}
                            <div
                                style="width: 64px;
                                height: 96px"
                            >
                                {#if result.media_type === "person"}
                                    <svg
                                        class="relative m-auto w-full h-full"
                                        aria-hidden="true"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                    >
                                        <path
                                            stroke="currentColor"
                                            stroke-width="1"
                                            d="M7 17v1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1a3 3 0 0 0-3-3h-4a3 3 0 0 0-3 3Zm8-9a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                        />
                                    </svg>
                                {:else}
                                    <svg
                                        class="relative m-auto w-full h-full text-white"
                                        aria-hidden="true"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                    >
                                        <path
                                            stroke="currentColor"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="1"
                                            d="M14 6H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1Zm7 11-6-2V9l6-2v10Z"
                                        />
                                    </svg>
                                {/if}
                            </div>
                        {:else}
                            <img
                                class="object-scale-down"
                                src={result.imageUrl}
                                alt={result.name}
                                style="width: 64px;
                                height: 96px"
                            />
                        {/if}
                        <div class="w-full px-4 my-auto flex flex-col">
                            <p style="font-weight: 700;">
                                {result.name}
                            </p>
                            {#if result.genres !== null && result.genres.length > 0}
                                <div class="flex flex-row w-fit">
                                    {#each result.genres as genre}
                                        <Badge
                                            class="text-white mr-1"
                                            variant="outline">{genre}</Badge
                                        >
                                    {/each}
                                </div>
                            {/if}
                            <p style="font-weight: 400;">
                                {result.releaseDate}
                            </p>
                        </div>
                    </div>
                    <Separator class="opacity-10" />
                {/each}
            </ScrollArea>
        {/if}
    </div>
    <div class="relative top-0 ml-auto">
        <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild let:builder>
                <Button
                    builders={[builder]}
                    variant="outline"
                    size="icon"
                    class="overflow-hidden rounded-full"
                >
                    <img
                        src=""
                        width={36}
                        height={36}
                        alt="Avatar"
                        class="overflow-hidden rounded-full"
                    />
                </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content align="end">
                <DropdownMenu.Label>My Account</DropdownMenu.Label>
                <DropdownMenu.Separator />
                <DropdownMenu.Item>Settings</DropdownMenu.Item>
                <DropdownMenu.Item>Support</DropdownMenu.Item>
                <DropdownMenu.Separator />
                <DropdownMenu.Item>Logout</DropdownMenu.Item>
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    </div>
</header>
