<script>
	import { Dialog as SheetPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.ts";
	let className = undefined;
	export { className as class };
</script>

<SheetPrimitive.Description class={cn("text-muted-foreground text-sm", className)} {...$$restProps}>
	<slot />
</SheetPrimitive.Description>
