import { index, int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

export const analyses = mysqlTable("analyses", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  contentType: mysqlEnum("contentType", ["post", "carrossel", "reel", "copy"]).notNull(),
  contentText: text("contentText").notNull(),
  product: varchar("product", { length: 300 }).notNull(),
  objective: varchar("objective", { length: 300 }).notNull(),
  targetAudience: text("targetAudience").notNull(),
  mediaUrl: text("mediaUrl"),
  mediaKey: varchar("mediaKey", { length: 1024 }),
  mediaMimeType: varchar("mediaMimeType", { length: 120 }),
  sourceUrl: text("sourceUrl"),
  sourceKind: mysqlEnum("sourceKind", ["direct_media", "published_post"]),
  sourceMediaMimeType: varchar("sourceMediaMimeType", { length: 120 }),
  status: mysqlEnum("status", ["processing", "completed", "needs_content", "failed"]).default("processing").notNull(),
  reportJson: text("reportJson"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Analysis = typeof analyses.$inferSelect;
export type InsertAnalysis = typeof analyses.$inferInsert;

export const instagramConnections = mysqlTable("instagramConnections", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  instagramUserId: varchar("instagramUserId", { length: 80 }),
  username: varchar("username", { length: 120 }),
  accountType: mysqlEnum("accountType", ["business", "creator"]).default("business").notNull(),
  status: mysqlEnum("status", ["ready", "connected", "expired", "revoked", "error"]).default("ready").notNull(),
  grantedScopes: text("grantedScopes"),
  accessTokenEncrypted: text("accessTokenEncrypted"),
  tokenExpiresAt: timestamp("tokenExpiresAt"),
  consentVersion: varchar("consentVersion", { length: 32 }),
  connectedAt: timestamp("connectedAt"),
  revokedAt: timestamp("revokedAt"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type InstagramConnection = typeof instagramConnections.$inferSelect;
export type InsertInstagramConnection = typeof instagramConnections.$inferInsert;

/**
 * Internal, admin-curated material used by the Observatório Platéia.
 * This knowledge base is intentionally separate from end-user analyses and
 * from any future behavioural evidence produced by Freud.
 */
export const observatoryReferences = mysqlTable("observatoryReferences", {
  id: int("id").autoincrement().primaryKey(),
  createdByUserId: int("createdByUserId").notNull(),
  title: varchar("title", { length: 240 }).notNull(),
  creator: varchar("creator", { length: 160 }).notNull(),
  contentType: mysqlEnum("contentType", ["post", "carrossel", "reel", "copy"]).notNull(),
  sourceKind: mysqlEnum("sourceKind", ["upload", "direct_media", "published_post", "copy"]).notNull(),
  sourceUrl: text("sourceUrl"),
  contentText: text("contentText").notNull(),
  mediaUrl: text("mediaUrl"),
  mediaKey: varchar("mediaKey", { length: 1024 }),
  mediaMimeType: varchar("mediaMimeType", { length: 120 }),
  segmentHint: varchar("segmentHint", { length: 240 }).notNull(),
  objectiveHint: varchar("objectiveHint", { length: 240 }).notNull(),
  metricsJson: text("metricsJson"),
  status: mysqlEnum("status", ["processing", "analyzed", "needs_content", "failed"]).default("processing").notNull(),
  classificationJson: text("classificationJson"),
  analysisJson: text("analysisJson"),
  promptVersion: varchar("promptVersion", { length: 32 }).default("2.0").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, table => ({
  createdAtIdx: index("observatoryReferences_createdAt_idx").on(table.createdAt),
  statusIdx: index("observatoryReferences_status_idx").on(table.status),
  contentTypeIdx: index("observatoryReferences_contentType_idx").on(table.contentType),
}));

export type ObservatoryReference = typeof observatoryReferences.$inferSelect;
export type InsertObservatoryReference = typeof observatoryReferences.$inferInsert;

/**
 * Versioned hypotheses and patterns promoted from multiple comparable
 * references. One observation is never enough to create a validated pattern.
 */
export const observatoryPatterns = mysqlTable("observatoryPatterns", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 180 }).notNull(),
  stage: mysqlEnum("stage", ["observation", "hypothesis", "provisional", "validated", "contradicted", "obsolete"]).default("hypothesis").notNull(),
  creativeFamily: varchar("creativeFamily", { length: 120 }).notNull(),
  objective: varchar("objective", { length: 160 }).notNull(),
  segment: varchar("segment", { length: 160 }).notNull(),
  mechanism: text("mechanism").notNull(),
  conditionsJson: text("conditionsJson"),
  evidenceJson: text("evidenceJson"),
  supportingCount: int("supportingCount").default(0).notNull(),
  counterexampleCount: int("counterexampleCount").default(0).notNull(),
  confidence: mysqlEnum("confidence", ["low", "medium", "high"]).default("low").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, table => ({
  stageIdx: index("observatoryPatterns_stage_idx").on(table.stage),
  familyIdx: index("observatoryPatterns_family_idx").on(table.creativeFamily),
}));

export type ObservatoryPattern = typeof observatoryPatterns.$inferSelect;
export type InsertObservatoryPattern = typeof observatoryPatterns.$inferInsert;
