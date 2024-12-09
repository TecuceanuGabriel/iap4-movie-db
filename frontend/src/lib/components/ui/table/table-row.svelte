<script>
	import { cn } from "$lib/utils.ts";
	let className = undefined;
	export { className as class };
</script>

<tr
	class={cn(
		"hover:bg-muted/50 data-[state=selected]:bg-muted border-b transition-colors",
		className
	)}
	{...$$restProps}
	on:click
	on:keydown
>
	<slot />
</tr>
