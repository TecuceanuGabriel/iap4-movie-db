<script lang="ts">
    import { Icons } from "$lib/components/icons/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { cn } from "$lib/utils.ts";

    let className: string | undefined | null = undefined;
    export { className as class };

    let isLoading = false;
    async function onSubmit() {
        isLoading = true;

        setTimeout(() => {
            isLoading = false;
        }, 3000);
    }
</script>

<div
    class="fixed overflow-hidden mx-auto flex flex-row drop-shadow-xl"
    style="inset: 20%;"
>
    <!-- Left panel -->
    <div
        class="text-white hidden lg:block lg:w-1/2 bg-cover bg-center bg-no-repeat bg-[url('https://images.unsplash.com/photo-1590069261209-f8e9b8642343?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1376&q=80')]"
    >
        <div class="flex flex-col justify-between p-4 h-full drop-shadow-xl">
            <div
                class="relative z-20 flex items-center text-lg font-medium text-top"
            >
                Acme Inc
            </div>
            <div class="relative z-20 mt-auto text-bottom">
                <blockquote class="space-y-2">
                    <p class="text-lg max-w-prose text-pretty">
                        &ldquo;This library has saved me countless hours of work
                        and helped me deliver stunning designs to my clients
                        faster than ever before. Highly recommended!&rdquo;
                    </p>
                    <footer class="text-sm">Sofia Davis</footer>
                </blockquote>
            </div>
        </div>
    </div>

    <!-- Right panel -->
    <div class="g:p-8 flex-1">
        <div
            class="mx-auto flex flex-col justify-center space-y-6 sm:w-[350px]"
        >
            <div class="flex flex-col space-y-2 text-center">
                <h1 class="text-2xl font-semibold tracking-tight">
                    Create an account
                </h1>
                <p class="text-muted-foreground text-sm">
                    Enter your email below to create your account
                </p>
            </div>
            <div class={cn("grid gap-6", className)} {...$$restProps}>
                <form on:submit|preventDefault={onSubmit}>
                    <div class="grid gap-2">
                        <div class="grid gap-1">
                            <Label class="sr-only" for="email">Email</Label>
                            <Input
                                id="email"
                                placeholder="name@example.com"
                                type="email"
                                autocapitalize="none"
                                autocomplete="email"
                                autocorrect="off"
                                disabled={isLoading}
                            />
                        </div>
                        <Button type="submit" disabled={isLoading}>
                            {#if isLoading}
                                <Icons.spinner
                                    class="mr-2 h-4 w-4 animate-spin"
                                />
                            {/if}
                            Sign In with Email
                        </Button>
                    </div>
                </form>
            </div>

            <p class="text-muted-foreground px-8 text-center text-sm">
                By clicking continue, you agree to our
                <a
                    href=""
                    class="hover:text-primary underline underline-offset-4"
                >
                    Terms of Service
                </a>
                and
                <a
                    href="#"
                    class="hover:text-primary underline underline-offset-4"
                >
                    Privacy Policy
                </a>
                .
            </p>
        </div>
    </div>
</div>
