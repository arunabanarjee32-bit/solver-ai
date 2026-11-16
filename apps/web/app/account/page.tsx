import { AccountForm } from "@/features/accounts/account-form";

export default async function AccountPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string | string[] }>;
}) {
  const params = await searchParams;
  return (
    <AccountForm
      nextPath={typeof params.next === "string" ? params.next : "/"}
    />
  );
}
