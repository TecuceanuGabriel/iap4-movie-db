<script lang="ts">
    import Star from "./components/Star.svelte";

    export let startingValue: number;
    export let onSubmit;

    let config = {
        readOnly: false,
        countStars: 5,
        range: { min: 0, max: 5, step: 0.001 },
        score: startingValue,
        showScore: true,
        name: "stars",
        scoreFormat: function () {
            return `(${this.score.toFixed(1)}/${this.countStars})`;
        },
        starConfig: {
            size: 30,
            fillColor: "rgba(250, 204, 21, 255)",
            strokeColor: "rgba(255, 255, 255, 0)",
            unfilledColor: "rgba(0, 0, 0, 255)",
            strokeUnfilledColor: "rgba(255, 255, 255, 0)",
        },
    };

    export function setValue(newValue) {
        config.score = newValue;
    }
</script>

<section class="stars-container">
    <div
        class="range-stars backdrop-blur-lg"
        role="slider"
        aria-valuemin={config.range.min}
        aria-valuemax={config.range.max}
        aria-valuenow={config.score}
        aria-valuetext={`Value: ${config.score}`}
        tabindex="0"
    >
        <div class="stars space-x-1">
            {#each Array(config.countStars) as star, id}
                {#if Math.floor(config.score) == id}
                    <Star
                        id={config.name + id}
                        readOnly={config.readOnly}
                        starConfig={config.starConfig}
                        fillPercentage={config.score - Math.floor(config.score)}
                    />
                {:else if Math.floor(config.score) > id}
                    <Star
                        id={config.name + id}
                        readOnly={config.readOnly}
                        starConfig={config.starConfig}
                        fillPercentage={1}
                    />
                {:else}
                    <Star
                        id={config.name + id}
                        readOnly={config.readOnly}
                        starConfig={config.starConfig}
                        fillPercentage={0}
                    />
                {/if}
            {/each}
        </div>
        <input
            name={config.name}
            class="slider"
            type="range"
            min={config.readOnly ? config.score : config.range.min}
            max={config.readOnly ? config.score : config.range.max}
            step={`${config.range.step}` || "0.5"}
            bind:value={config.score}
            on:change
            on:click={() => {
                try {
                    onSubmit(config.score);
                } catch (e) {
                    config.score = 0;
                }
            }}
        />
    </div>
    {#if config.showScore}
        <span
            class="text-muted-foreground"
            style="font-size: {config.starConfig.size / 2}px;"
        >
            {#if config.scoreFormat}
                {config.scoreFormat()}
            {:else}
                ({((config.score / config.countStars) * 100).toFixed(2)}%)
            {/if}
        </span>
    {/if}
</section>

<style>
    .stars-container {
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .range-stars {
        position: relative;
    }
    .stars {
        display: flex;
        gap: 0.5rem;
    }
    .slider {
        opacity: 0;
        cursor: pointer;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        left: 0;
        height: 100%;
    }
</style>
