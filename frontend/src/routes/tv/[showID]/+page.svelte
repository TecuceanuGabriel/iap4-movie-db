<script>
    import Autoplay from "embla-carousel-autoplay";
    import { onMount } from "svelte";
    import { cubicInOut } from "svelte/easing";
    import {
        apiKey,
        imgBaseUrl,
        imgOriginal,
        topGradientSoftness,
        bottomGradientSoftness,
        updateWindowHeight,
        clamp,
        formatCurrency,
        imgSizeSmall,
        redirectTo,
    } from "$lib/utils";
    import { fade } from "svelte/transition";
    import { page } from "$app/stores";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import * as Carousel from "$lib/components/ui/carousel/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import { Video } from "lucide-svelte";

    const showID = $page.params.showID;
    let show = null;
    let images = null;
    let recs = null;
    let primaryImageSize = 50;

    onMount(async () => {
        updateWindowHeight();
        window.addEventListener("resize", updateWindowHeight);

        try {
            const response = await fetch(`${apiKey}/tv/details/${showID}`);
            if (!response.ok) {
                throw new Error(
                    `Could not get show details: ${response.status}`,
                );
            }

            const data = await response.json();
            let backdropUrl = `${imgBaseUrl}/${imgOriginal}${data.backdrop_path}`;
            let posterUrl = `${imgBaseUrl}/${imgOriginal}${data.poster_path}`;
            show = {
                ...data,
                backdropUrl: backdropUrl,
                posterUrl: posterUrl,
            };
            console.log(show);
        } catch (e) {
            console.log(e);
        }

        try {
            const response = await fetch(`${apiKey}/tv/${showID}/images`);
            if (!response.ok) {
                throw new Error(
                    `Could not get show images: ${response.status}`,
                );
            }

            const data = await response.json();
            images = data.backdrops.map(
                (url) => `${imgBaseUrl}/${imgOriginal}${url.file_path}`,
            );
            console.log(images);
        } catch (e) {
            console.log(e);
        }

        try {
            const response = await fetch(
                `${apiKey}/tv/${showID}/recommendations`,
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get movie details: ${response.status}`,
                );
            }

            const data = await response.json();
            recs = data.results.map((rec) => {
                return {
                    id: rec.id,
                    posterUrl: `${imgBaseUrl}/${imgSizeSmall}${rec.poster_path}`,
                };
            });
            console.log(recs);
        } catch (e) {
            console.log(e);
        }

        return () => {
            window.removeEventListener("resize", updateWindowHeight);
        };
    });
</script>

{#if show !== null}
    <div
        class="z-0 absolute top-0 left-0 w-full h-[{primaryImageSize}vh] bg-cover bg-center bg-no-repeat opacity-55"
        style="height: {primaryImageSize}rem;
               font-family: 'Open Sans';
               background-image: url('{show.backdropUrl}');"
    >
        <div
            class="absolute top-[0vh] bg-easing-t-smooth_fade w-full"
            style="height: {topGradientSoftness}vh"
        ></div>

        <div
            class="absolute w-full bg-easing-b-smooth_fade"
            style="bottom: 0rem;
                   height: {bottomGradientSoftness * primaryImageSize}rem;
                   "
        ></div>

        <div
            class="absolute top-0 bg-gradient-to-r from-rich_black to-rich_black/0 w-full"
            style="opacity: 0.9;
                   height: {primaryImageSize}rem;"
        ></div>

        <div
            class="absolute top-0 bg-gradient-to-l from-rich_black to-rich_black/0 w-full"
            style="opacity: 0.9;
                   height: {primaryImageSize}rem;"
        ></div>
    </div>
    <div
        class="relative flex flex-col inset-0 mx-auto w-fit h-fit drop-shadow-lg pb-8"
        style="padding-top: {clamp(
            primaryImageSize / 2,
            0,
            primaryImageSize,
        )}vh;"
    >
        <div class="relative flex flex-row space-x-4">
            <img
                src={show.posterUrl}
                class="h-auto max-w-xs"
                alt={show.original_name}
            />
            <div class="flex flex-col w-[800px] space-y-2">
                <div class="flex flex-row space-x-2 items-end">
                    <h1 class="text-4xl" style="font-weight: 700">
                        {show.original_name}
                    </h1>
                    <p class="text-muted-foreground">
                        {#if show.status !== null}
                            {show.status.toLowerCase()}
                        {/if}
                    </p>
                </div>
                <p class="text-xl">{show.tagline}</p>
                <div class="flex flex-row">
                    {#each show.genres as genre}
                        <Badge class="text-white mr-1" variant="outline"
                            >{genre.name}
                        </Badge>
                    {/each}
                </div>
                <div class="flex flex-row space-x-1">
                    <p>Rating: {show.vote_average}</p>
                    <svg
                        class="w-6 h-6 text-white"
                        aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <path
                            stroke="currentColor"
                            stroke-width="2"
                            d="M11.083 5.104c.35-.8 1.485-.8 1.834 0l1.752 4.022a1 1 0 0 0 .84.597l4.463.342c.9.069 1.255 1.2.556 1.771l-3.33 2.723a1 1 0 0 0-.337 1.016l1.03 4.119c.214.858-.71 1.552-1.474 1.106l-3.913-2.281a1 1 0 0 0-1.008 0L7.583 20.8c-.764.446-1.688-.248-1.474-1.106l1.03-4.119A1 1 0 0 0 6.8 14.56l-3.33-2.723c-.698-.571-.342-1.702.557-1.771l4.462-.342a1 1 0 0 0 .84-.597l1.753-4.022Z"
                        />
                    </svg>
                    <p>from {show.vote_count} votes</p>
                </div>

                <Separator class="opacity-50"></Separator>
                <p class="text-justify text-xl">{show.overview}</p>
            </div>
        </div>

        <div class="flex flex-col">
            <div class="relative mt-12 flex flex-col justify-center space-y-3">
                <h1 class="text-4xl" style="font-weight: 700;">Media</h1>
                <Carousel.Root
                    plugins={[
                        Autoplay({
                            delay: 5000,
                            stopOnInteraction: true,
                        }),
                    ]}
                    class="relative mx-auto w-[80vw]"
                >
                    <Carousel.Content class="-ml-1">
                        {#each images as image}
                            <Carousel.Item
                                class="pl-1 md:basis-1/2 lg:basis-1/3"
                            >
                                <div class="p-1">
                                    <img
                                        class="h-auto max-w-full rounded-lg"
                                        src={image}
                                        alt=""
                                    />
                                </div>
                            </Carousel.Item>
                        {/each}
                    </Carousel.Content>
                    <Carousel.Previous class="bg-transparent" />
                    <Carousel.Next class="bg-transparent" />
                </Carousel.Root>
            </div>

            <!-- svelte-ignore a11y_no_static_element_interactions -->
            {#if recs !== null && recs.length > 0}
                <div
                    class="relative mt-12 flex flex-col justify-center space-y-3"
                    on:click={(event) => {
                        console.log(event.target);
                        if (event.target.tagName === "IMG")
                            redirectTo(`/tv/${event.target.dataset.id}`);
                    }}
                    on:keydown={(event) => {
                        if (
                            event.target.tagName === "IMG" &&
                            event.key === "Enter"
                        )
                            redirectTo(`/tv/${event.target.dataset.id}`);
                    }}
                >
                    <h1 class="text-4xl" style="font-weight: 700;">Similar</h1>
                    <Carousel.Root
                        plugins={[
                            Autoplay({
                                delay: 5000,
                                stopOnInteraction: true,
                            }),
                        ]}
                        class="relative mx-auto w-[80vw]"
                    >
                        <Carousel.Content class="-ml-1">
                            {#each recs as rec}
                                <Carousel.Item
                                    class="cursor-pointer w-fit md:basis-1/2 lg:basis-1/5"
                                    tabindex="0"
                                    role="button"
                                >
                                    <img
                                        class="h-auto max-w-full rounded-lg"
                                        src={rec.posterUrl}
                                        data-id={rec.id}
                                        alt=""
                                    />
                                </Carousel.Item>
                            {/each}
                        </Carousel.Content>
                        <Carousel.Previous class="bg-transparent" />
                        <Carousel.Next class="bg-transparent" />
                    </Carousel.Root>
                </div>
            {/if}
        </div>
    </div>
{/if}
