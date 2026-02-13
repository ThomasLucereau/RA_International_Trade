prompt_1 = """You are assisting me in analyzing companies ' earnings calls . The transcript of the earnings call will be supplied as a plain text in the user prompt . Your goal is to determine whether the company discusses impacts on its business due to various economic policies . We define each in turn .

A. Tariffs are defined as taxes imposed on imported foreign goods . In order to be considered tariffs , these policies must be imposed by the importing country to be classified as tariffs .
B. Sanctions are government - imposed restrictions on trade or financial transactions designed to coerce , punish , or deter targeted firms or governments .
C. Export controls are defined as restrictions on which countries or foreign firms a company is allowed to sell their goods or services to. In order to be considered export controls , these policies must be imposed by the exporting countries , in contrast to import tariffs , which are instead taxes imposed by the importing country D. Boycotts are defined as a form of protest in which individuals or groups refuse to buy or use products or services of a firm as a way to express disapproval or to force change . It is typically viewed as voluntary and as a social method to influence business practices , government policies , or social issues but may be officially encouraged .
E. Investment Screening is a regulatory review carried out by government agencies to evaluate whether potential foreign investments meet certain criteria before allowing the investment to take place . Authorities review foreign investments ( including mergers and acquisitions ) to ensure they do not pose risks to national security , critical infrastructure , or public interests . Investment Screening can be on inbound ( foreign investment in the domestic economy ) or outbound ( domestic investment in a foreign economy ) investments . In order to be considered investment screening , the policy needs to be carried out by the government . Do not consider private firms analyzing whether a particular investment is a good idea or profitable to be investment screening .
F. Subsidies to onshore or friendshore production are financial incentives provided by governments to encourage companies to manufacture goods domestically ( onshoring ) or in allied or politically aligned countries ( friendshoring ) rather than in less trusted or adversarial nations . These subsidies can take various forms , such as: direct grants or tax breaks for building or expanding production facilities , research and development support to boost innovation in key sectors , preferential loans or guarantees to reduce the cost of doing business locally or in partner countries , procurement preferences for products made in certain locations . Please do not include general subsidies unrelated to the goal of moving production to a particular country as part of this definition .
G. Geoeconomic pressure is the use of economic relationships by governments to achieve geopolitical or economic ends . For example , such pressure can take the form of tariffs , sanctions , boycotts , investment screening , or subsidies to onshore or friendshore .

## Response Instructions : Part 1 ( Structured JSON Output ) ##
The first part of your response should be a structured output in JSON format that recaps
your analysis in a structured way . This part of your response should be enclosed between the tags <JSON > and </JSON >. The JSON output must have the following fields exactly . Please make sure to enforce the JSON schema specified below strictly : i.e., the column names should correspond exactly to those listed below :
1. A boolean flag called " tariffs_any ", which should be 1 if the firm explicitly or implicitly discusses tariffs at any point in the call , and 0 otherwise .
2. A boolean flag called " sanctions_any ", which should be 1 if the firm explicitly or implicitly discusses sanctions at any point in the call , and 0 otherwise . Do not classify tariffs ( taxes on imports ) as sanctions .
3. A boolean flag called " export_controls_any ", which should be 1 if the firm explicitly or implicitly discusses export controls at any point in the call , and 0 otherwise . Do not classify tariffs ( taxes on imports ) as export controls .
4. A boolean flag called " boycotts_any ", which should be 1 if the firm explicitly or implicitly discusses boycotts at any point in the call , and 0 otherwise . Do not classify restrictions imposed by governments by law or regulations as boycotts .
5. A boolean flag called " investment_screening_any ", which should be 1 if the firm explicitly or implicitly discusses investment screening at any point in the call , and 0 otherwise .
6. A boolean flag called " geo_subsidies_any ", which should be 1 if the firm explicitly or implicitly discusses subsidies for onshoring or friendshoring at any point in the call , and 0 otherwise .
7. A boolean flag called " geoeconomic_any ", which should be 1 if the firm explicitly or implicitly discusses any form of geoeconomic pressure (as defined above ) during the call , and 0 otherwise . The term geoeconomic or geoeconomics are unlikely to be used explicitly during the call and any discussion is instead likely to involve the underlying policies such as tariffs , sanctions , export controls , boycotts , investment screening , and subsidies to onshore or friendshore . You should return a 1 if the firm discusses impacts on its business that clearly relate to geoeconomic pressure .

## Response Instructions : Part 2 ##
Write a single summary of 750 words or fewer that captures only how the firm is (or may be) affected by the set of geoeconomic policies discussed in the analysis above , including but not limited to as tariffs , export controls , financial and trade sanctions , boycotts , investment screening , travel restrictions , subsidies to onshore or friendshore . Omit all unrelated content . If the firm is not affected by any of these policies , write " Not affected ." Enclose this analysis between the tags <
SUMMARY > and </ SUMMARY >.
## Important Notes : ##
- Discussions may be explicit , such as directly mentioning " tariffs ," " sanctions ," or specific policy names .
- Discussions may be indirect , referring to impacts like inability to trade with certain countries , compliance with new export regulations , or financial losses due to exiting a sanctioned market .
- Do not consider general market volatility , economic downturns , or supply chain and travel or shipping issues unrelated to the above policies as indications of geoeconomic policies .
## Examples of Relevant Discussions : ##
- Mentioning increased costs due to new tariffs on imported materials .
- Discussing loss of a market due to trade sanctions against a country (e.g., exits from Russia due to sanctions following the Russia - Ukraine conflict ).
- Referring to compliance challenges with new export controls .
- Mention the risk that an investment might not be approved due to failing the investment screening review .
- Receiving a subsidy to relocate production to the domestic economy or away from a country that is considered potentially hostile .
## Examples of Non - Relevant Discussions : ##
- Talking about decreased sales due to a general economic recession .
- Discussing delays caused by a natural disaster . - Discussing purely domestic regulations (e.g., changes in US domestic tax laws or
Federal Reserve policies ).
- Mentioning fluctuations in currency exchange rates .
## Ensure you : ##
- Use the tags exactly as written .
- Choose a boolean flag (0 or 1) that is consistent with your analysis .
- Do not interpret general economic issues as geoeconomic policies unless directly
linked .
"""