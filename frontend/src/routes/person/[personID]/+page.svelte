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
        shuffle,
    } from "$lib/utils";
    import { fade } from "svelte/transition";
    import { page } from "$app/stores";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import * as Carousel from "$lib/components/ui/carousel/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import { Video } from "lucide-svelte";
    import { tv } from "tailwind-variants";
    import CollapsibleText from "$lib/components/ui/collapsible-text/index";

    const personID = $page.params.personID;
    let person = null;
    let credits = null;
    let images = null;
    let recs = null;
    let primaryImageSize = 50;

    onMount(async () => {
        updateWindowHeight();
        window.addEventListener("resize", updateWindowHeight);

        try {
            const creditsResponse = await fetch(
                `${apiKey}/person/${personID}/credits`,
            );
            if (!creditsResponse.ok) {
                throw new Error(
                    `Could not get person movie credits: ${creditsResponse.status}`,
                );
            }
            let creditsData = await creditsResponse.json();
            credits = creditsData.cast
                .filter((credit) => credit.poster_path !== null)
                .map((credit) => {
                    return {
                        ...credit,
                        posterUrl: `${imgBaseUrl}/${imgOriginal}${credit.poster_path}`,
                    };
                });
        } catch (e) {
            console.log(e);
        }

        try {
            const response = await fetch(
                `${apiKey}/person/details/${personID}`,
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get person details: ${response.status}`,
                );
            }
            const data = await response.json();

            person = {
                ...data,
                backdropUrl: `${imgBaseUrl}/${imgOriginal}${credits[0].backdrop_path}`,
                posterUrl: `${imgBaseUrl}/${imgOriginal}${data.profile_path}`,
            };
        } catch (e) {
            console.log(e);
        }

        try {
            const response = await fetch(`${apiKey}/person/${personID}/images`);
            if (!response.ok) {
                throw new Error(
                    `Could not get show images: ${response.status}`,
                );
            }

            const data = await response.json();
            images = data.profiles.map(
                (url) => `${imgBaseUrl}/${imgOriginal}${url.file_path}`,
            );
            images.shift();
        } catch (e) {
            console.log(e);
        }

        return () => {
            window.removeEventListener("resize", updateWindowHeight);
        };
    });

    const content =
        "Lorem ipsum dolor sit amet, consectetur adippscing elit. Duis eu neque lacus. Mauris scelerisque sed arcu vel pharetra. Aenean nec nulla sed nulla viverra cursus at et lacus. Etiam accumsan turpis ac consequat sodales. In sollicitudin egestas arcu, et vulputate nunc semper in. Praesent interdum odio ac tempor feugiat. Integer id sapien a enim iaculis fringilla sed ac lacus. Vivamus odio enim, faucibus vitae nibh malesuada, semper dapibus massa. Fusce ligula lorem, dictum sit amet elit sit amet, tempor feugiat nulla. Vestibulum non luctus dolor. Vestibulum consectetur ipsum nec sem eleifend ultricies. Lorem ipsum dolor.";
</script>

{#if person !== null}
    <div
        class="z-0 absolute top-0 left-0 w-full h-[{primaryImageSize}vh] bg-cover bg-center bg-no-repeat opacity-55"
        style="height: {primaryImageSize}rem;
               font-family: 'Open Sans';
               background-image: url('{person.backdropUrl}');"
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
                src={person.posterUrl}
                class="h-full max-w-xs"
                alt={person.name}
            />
            <div class="flex flex-col w-[800px] space-y-2 text-xl">
                <h1 class="text-4xl" style="font-weight: 700">
                    {person.name}
                </h1>
                <p>Born {person.birthday}, {person.place_of_birth}</p>
                {#if person.deathday !== null}
                    <p>Died {person.deathday}</p>
                {/if}
                <CollapsibleText
                    textContent={person.biography}
                    maxWords={100}
                    readMoreLabel="more"
                    readLessLabel="less"
                    additional="text-xl"
                />
            </div>
        </div>

        <div class="flex flex-col">
            {#if images !== null && images.length > 0}
                <div
                    class="relative mt-12 flex flex-col justify-center space-y-3"
                >
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
                                    class="pl-1 md:basis-1/2 lg:basis-1/5"
                                >
                                    <div class="p-1">
                                        <img
                                            width="400"
                                            height="200"
                                            class="rounded-lg"
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
            {/if}

            {#if credits !== null && credits.length > 0}
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <div
                    class="relative mt-12 flex flex-col justify-center space-y-3"
                    on:click={(event) => {
                        if (event.target.tagName === "IMG")
                            redirectTo(
                                `/${event.target.dataset.type}/${event.target.dataset.id}`,
                            );
                    }}
                    on:keydown={(event) => {
                        if (
                            event.target.tagName === "IMG" &&
                            event.key === "Enter"
                        )
                            redirectTo(
                                `/${event.target.type}/${event.target.id}`,
                            );
                    }}
                >
                    <h1 class="text-4xl" style="font-weight: 700;">
                        Credited in
                    </h1>
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
                            {#each credits as credit}
                                <Carousel.Item
                                    class="cursor-pointer w-fit md:basis-1/2 lg:basis-1/5"
                                    tabindex="0"
                                    role="button"
                                >
                                    <img
                                        class="h-auto max-w-full rounded-lg"
                                        src={credit.posterUrl}
                                        data-id={credit.id}
                                        data-type={credit.media_type}
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
