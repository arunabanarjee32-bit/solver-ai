import { Workspace } from "@/features/practice/workspace";
export default async function ProblemRoute({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <Workspace slug={slug} />;
}
